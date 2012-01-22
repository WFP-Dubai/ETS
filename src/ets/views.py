import datetime
import pyqrcode
import cStringIO
import os
import decimal
from subprocess import call, Popen
from itertools import chain

from django import forms
from django.db.models import Q
#from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
#from django.core import serializers
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.http import Http404
from django.conf import settings
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import apply_extra_context
from django.contrib import messages
from django.db import transaction
from django.utils.dateformat import format
from django.utils.translation import ugettext as _
from django.core.management import call_command
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import FormView
from django.core import serializers

from ets.forms import WaybillRecieptForm, BaseLoadingDetailFormSet, DispatchWaybillForm
from ets.forms import WaybillSearchForm, LoadingDetailDispatchForm #, WaybillValidationFormset 
from ets.forms import LoadingDetailRecieptForm, WaybillScanForm, DateRangeForm, ImportDataForm
from .decorators import person_required, officer_required, dispatch_view, receipt_view, waybill_user_related 
from .decorators import warehouse_related, dispatch_compas, receipt_compas
import ets.models
from .utils import history_list, send_dispatched, send_received, _data_to_response, import_file
from .compress import compress_json, decompress_json
import simplejson


def waybill_detail(request, waybill, template="waybill/detail.html", extra_context=None):
    """utility that shows waybill's details"""    
    
    loading_log = ets.models.LoadingDetail.audit_log.filter(waybill=waybill)
    waybill_log = waybill.audit_log.all()

    #Recepient should not see dispatcher's history
    if not waybill.order.warehouse.persons.filter(pk=request.user.pk).count():
        persons = waybill.order.warehouse.get_persons()
        waybill_log = waybill_log.exclude(action_user__in=persons)
        loading_log = loading_log.exclude(action_user__in=persons)
        
    loading_details = ((loading, history_list(loading_log.filter(stock_item=loading.stock_item), ets.models.LoadingDetail))
                        for loading in waybill.loading_details.all())
    
    context = {
        'object': waybill,
        'items': waybill.loading_details.select_related(),
        'waybill_history': history_list(waybill_log, ets.models.Waybill, ('date_modified',)),
        'loading_detail_history': loading_details,
    }
    apply_extra_context(extra_context or {}, context)
    return direct_to_template(request, template, context)


@waybill_user_related
def waybill_view(request, waybill_pk, queryset, template):
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    return waybill_detail(request, waybill, template)
    

@require_POST
@person_required
@dispatch_view
def waybill_finalize_dispatch(request, waybill_pk, queryset):
    """
    called when user pushes Print Original on dispatch
    Redirects to order details
    """
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.dispatch_sign()
    
    messages.add_message(request, messages.INFO, _('Waybill %(waybill)s Dispatch Signed') % {
        "waybill": waybill.pk
    })
    
    return waybill_detail(request, waybill, extra_context={'print_original': True})


@waybill_user_related
def waybill_list(request, queryset, template='waybill/list.html', extra_context=None):
    """Shows waybill listing"""
    context = {'object_list': queryset,}
    apply_extra_context(extra_context or {}, context)
    return direct_to_template(request, template, context)

def waybill_search( request, form_class=WaybillSearchForm, 
                    queryset=ets.models.Waybill.objects.all(), 
                    template='waybill/list.html'):
#                    param_name='wbnumber', consegnee_code='W200000475' ):
    
    form = form_class(request.GET or None)
    search_string = form.cleaned_data['q'] if form.is_valid() else ''
    queryset = queryset.filter(pk__icontains=search_string)
    
    return waybill_list(request, queryset=queryset)


@transaction.commit_on_success
def _dispatching(request, waybill, template, success_message, form_class=DispatchWaybillForm, 
                formset_form=LoadingDetailDispatchForm, formset_class=BaseLoadingDetailFormSet):
    """Private function with common functionality for creating and editing dispatching waybill"""
    order = waybill.order
    
    class FormsetForm(formset_form):
        stock_item = forms.ModelChoiceField(queryset=order.get_stock_items(), label=_('Stock Item'))
        
    loading_formset = inlineformset_factory(ets.models.Waybill, ets.models.LoadingDetail, 
                       form=FormsetForm, formset=formset_class, 
                       extra=1, max_num=5,
                       can_order=False, can_delete=True)\
        (request.POST or None, request.FILES or None, prefix='item', instance=waybill)
    
    form = form_class(data=request.POST or None, files=request.FILES or None, instance=waybill)
    
    warehouses = ets.models.Warehouse.get_warehouses(order.location, order.consignee).exclude(pk=order.warehouse.pk)
    
    form.fields['destination'].queryset = warehouses
    form.fields['destination'].empty_label = None
    
    if form.is_valid() and loading_formset.is_valid():
        waybill = form.save()
        loading_formset.save()
        
        messages.success(request, success_message)
        return redirect(waybill)
        
    return direct_to_template( request, template, {
        'form': form, 
        'formset': loading_formset,
        'object': order,
        'waybill': waybill,
    })


@person_required
@warehouse_related
def waybill_create(request, order_pk, queryset, **kwargs):
    """Creates a Waybill"""
    
    order = get_object_or_404(queryset, pk=order_pk)
    waybill = ets.models.Waybill(order=order, dispatcher_person=request.user.person)

    return _dispatching(request, waybill, success_message=_("Waybill has been created"), **kwargs)


@person_required
@dispatch_view
def waybill_dispatch_edit(request, order_pk, waybill_pk, queryset, **kwargs):
    """Updates not signed dispatching waybill"""
    
    waybill = get_object_or_404(queryset, pk=waybill_pk, order__pk=order_pk)
    return _dispatching(request, waybill, success_message=_("Waybill has been updated"), **kwargs) 


@transaction.commit_on_success
def waybill_reception(request, waybill_pk, queryset, form_class=WaybillRecieptForm, 
                      formset_form = LoadingDetailRecieptForm,
                      template='waybill/receive.html'):
    waybill = get_object_or_404(queryset, pk=waybill_pk)
    waybill.receipt_person = request.user.person
    
    loading_formset = inlineformset_factory(ets.models.Waybill, ets.models.LoadingDetail, 
                                            form=formset_form, extra=0, max_num=5,
                                            can_order=False, can_delete=False)\
                                (request.POST or None, request.FILES or None, instance=waybill, prefix='item')
    
    today = datetime.date.today()
    form = form_class(data=request.POST or None, files=request.FILES or None, initial = {
        'arrival_date': today,
        'start_discharge_date': today,
        'end_discharge_date': today,
    }, instance=waybill)
    
    form.fields['destination'].queryset = request.user.person.warehouses.all().exclude(pk=waybill.order.warehouse.pk)
    
    if form.is_valid() and loading_formset.is_valid():
        waybill = form.save()
        loading_formset.save()
        
        messages.add_message(request, messages.INFO, _('Waybill has been discharged'))
        
        return redirect(waybill)
    
    return direct_to_template(request, template, {
        'form': form, 
        'formset': loading_formset,
        'waybill': waybill,
    })


@require_POST
@person_required
@receipt_view
def waybill_finalize_receipt(request, waybill_pk, queryset):
    """ Signs reception"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt_sign()
    
    messages.add_message( request, messages.INFO, _('Waybill %(waybill)s Receipt Signed') % { 
        'waybill': waybill.pk,
    })

    return waybill_detail(request, waybill, extra_context={'print_original': True})


@person_required
def waybill_reception_scanned(request, scanned_code, queryset):
    waybill = ets.models.Waybill.decompress(scanned_code)
    if not waybill:
        raise Http404
    return waybill_reception(request, waybill.pk, queryset)


@require_POST
@person_required
@dispatch_view
def waybill_delete(request, waybill_pk, queryset, redirect_to=''):
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.delete()
    redirect_to = redirect_to or request.GET.get('redirect_to', '')
        
    messages.info(request, _('Waybill %(number)s has now been Removed') % {"number": waybill.pk})

    if redirect_to:
        return redirect(redirect_to)
    elif request.META.has_key('HTTP_REFERER'):
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')
        

@officer_required
@dispatch_compas
def dispatch_validates(request, queryset, template):
    return direct_to_template(request, template, {
        'object_list': queryset.filter(validated=False),
        'validated_waybills': queryset.filter(validated=True),
    })

@officer_required
@receipt_compas
def receipt_validates(request, queryset, template):
    return direct_to_template(request, template, {
        'object_list': queryset.filter(receipt_validated=False),
        'validated_waybills': queryset.filter(receipt_validated=True),
    })


@require_POST
@officer_required
@dispatch_compas
def validate_dispatch(request, waybill_pk, queryset):
    """Sets 'validated' flag"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.validated = True
    waybill.save()
    
    messages.add_message(request, messages.INFO, 
                        _('Waybill %(waybill)s has been validated. It will be sent in few minutes.') % { 
                            'waybill': waybill.pk,
                        })

    return redirect('dispatch_validates')


@require_POST
@officer_required
@receipt_compas
def validate_receipt(request, waybill_pk, queryset):
    """Sets 'validated' flag"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt_validated = True
    waybill.save()
    
    messages.add_message(request, messages.INFO, 
                        _('Waybill %(waybill)s has been validated. It will be sent in few minutes.') % { 
                            'waybill': waybill.pk,
                        })

    return redirect('receipt_validates')


def deserialize(request, form_class=WaybillScanForm):
    form = form_class(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data['data']
        waybill = ets.models.Waybill.decompress(data)
        if waybill:
            if request.GET.get("receipt",""):
                return redirect('waybill_reception_scanned', scanned_code=data )
            return waybill_detail(request, waybill)

    messages.error(request, _('Incorrect Data !!!! Ensure a valid barcode information is pasted'))
    return redirect('index')


def barcode_qr( request, waybill_pk, queryset=ets.models.Waybill.objects.all() ):
    
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    
    file_out = cStringIO.StringIO()
    
    image = pyqrcode.MakeQRImage(waybill.compress(), minTypeNumber = 24, 
                                 errorCorrectLevel = pyqrcode.QRErrorCorrectLevel.L)
    image.save(file_out, 'JPEG')
    file_out.reset()
    
    result = file_out.read()
    
    file_out.close()
    
    return HttpResponse(result, mimetype="image/jpeg")


def stock_items(request, template_name, queryset):
    
    if not request.user.has_perm("ets.stockitem_api_full_access"):
        queryset = queryset.filter(Q(persons__pk=request.user.pk) | Q(compas__officers=request.user))
    
    return object_list(request, queryset, paginate_by=5, template_name=template_name)


def get_stock_data(request, queryset):
    
    object_pk = request.GET.get('stock_item')
    
    if not request.user.has_perm("ets.stockitem_api_full_access"):
        queryset = queryset.filter(Q(warehouse__persons__pk=request.user.pk) | Q(warehouse__compas__officers=request.user))
    
    stock_item = get_object_or_404(queryset, pk=object_pk)
    return HttpResponse(simplejson.dumps({
        'unit_weight_net': stock_item.unit_weight_net,
        'unit_weight_gross': stock_item.unit_weight_gross,
        'number_of_units': stock_item.number_of_units,
    }, use_decimal=True))

@permission_required("ets.sync_compas")
def sync_compas(request):
    
    #Execute external command
    Popen(['./bin/instance', 'sync_compas'], cwd=settings.EGG_ROOT) 
    
    return HttpResponse(format(ets.models.StockItem.get_last_update(), settings.DATETIME_FORMAT))

@permission_required("ets.sync_compas")
def view_logs(request, template_name="admin/logs.html"):
    
    from .management.commands import sync_compas
    from .management.commands import submit_waybills
    
    logs = []
    
    sync_command = sync_compas.Command()
    try:
        with open(sync_command.get_log_name()) as f:
            logs.append(('sync_compas', f.read() or _("Empty"), sync_command.help))
    except IOError:
        pass
    
    submit_command = submit_waybills.Command()
    try:
        with open(submit_command.get_log_name()) as f:
            logs.append(('submit_waybills', f.read() or _("Empty"), submit_command.help))
    except IOError:
        pass
    
    return direct_to_template(request, template=template_name, extra_context={'logs': logs})
    
@officer_required
@dispatch_compas
def send_dispatched_view(request, queryset):
    """Submits dispatch waybills to compas"""
    total = 0
    for waybill in queryset:
        send_dispatched(waybill)
        if waybill.sent_compas:
            total += 1
    
    messages.add_message(request, messages.INFO, 
                        _('Number of submitted waybills: %(total)s') % { 
                            'total': total,
                        })
    
    if len(queryset) - total:
        messages.add_message(request, messages.ERROR, 
                        _('Number of wrong waybills: %(count)s') % { 
                            'count': len(queryset) - total,
                        })
    
    return redirect('dispatch_validates')


@officer_required
@receipt_compas
def send_received_view(request, queryset):
    """Submits received waybills to compas"""
    for waybill in queryset:
        send_received(waybill)
    
    return redirect('receipt_validates')


class ExportDataBase(FormView):
    
    template_name = 'sync/export_file.html'
    form_class = DateRangeForm
    file_name = 'data-%(start_date)s-%(end_date)s'
    
    #===========================================================================
    # def get_context_data(self, **kwargs):
    #    context = super(ExportDataBase, self).get_context_data(**kwargs)
    #    context['']
    #===========================================================================
    
    def get_initial(self):
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)
        return {'start_date': start_date, 'end_date': end_date}
    
    def construct_data(self):
        raise NotImplementedError()
    
    def form_valid(self, form):
        start_date = form.cleaned_data['start_date'] 
        end_date = form.cleaned_data['end_date']
            
        return _data_to_response(self.construct_data(start_date, end_date), self.file_name % {
            'start_date': start_date, 
            'end_date': end_date,
        })
    

class ExportWaybillData(ExportDataBase):
    
    file_name = 'waybills-%(start_date)s-%(end_date)s'
    
    def construct_data(self, start_date, end_date):
        #Append log entry 
        return chain(
            ets.models.Waybill.objects.filter(date_modified__range=(start_date, end_date+datetime.timedelta(1))),
            ets.models.LoadingDetail.objects.filter(waybill__date_modified__range=(start_date, end_date+datetime.timedelta(1)),
                                                    waybill__date_removed__isnull=True)
        )


def export_compas_file(request):
    return _data_to_response(chain(
        ets.models.Organization.objects.all(),
        ets.models.Compas.objects.all(),
        ets.models.Location.objects.all(),
        ets.models.Person.objects.all(),
        ets.models.Warehouse.objects.filter(Q(end_date__lt=datetime.date.today) | Q(end_date__isnull=True), start_date__gte=datetime.date.today),
        ets.models.LossDamageType.objects.all(),
        ets.models.Commodity.objects.all(),
        ets.models.CommodityCategory.objects.all(),
        ets.models.Package.objects.all(),
        ets.models.StockItem.objects.all(),
        ets.models.Order.objects.filter(expiry__lte=datetime.date.today),
        ets.models.OrderItem.objects.filter(order__expiry__lte=datetime.date.today),
    ), 'ets_data-%s' % datetime.date.today())


class ImportData(FormView):
    
    template_name = 'sync/import_file.html'
    form_class = ImportDataForm
    
    def form_valid(self, form):
        _file = form.cleaned_data['file']

        import_file(_file)
        
        messages.add_message(self.request, messages.INFO, _('File has been imported successfully.'))
        
        return self.get(self.request)
