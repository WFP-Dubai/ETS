import datetime
from subprocess import Popen

from django import forms
from django.db.models import Q
from django.db.models.aggregates import Max
#from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormView
from django.core import serializers
from django.contrib.admin import models as log_models
from django.contrib.contenttypes.models import ContentType

from ets.forms import WaybillRecieptForm, BaseLoadingDetailFormSet, DispatchWaybillForm
from ets.forms import WaybillSearchForm, LoadingDetailDispatchForm #, WaybillValidationFormset 
from ets.forms import LoadingDetailReceiptForm, WaybillScanForm, ImportDataForm
from ets.decorators import person_required, officer_required, dispatch_view, receipt_view, waybill_user_related 
from ets.decorators import warehouse_related, dispatch_compas, receipt_compas
import ets.models
from ets.utils import history_list, send_dispatched, send_received, create_logentry, construct_change_message
from ets.utils import import_file, get_compas_data, data_to_file_response
from ets.pdf import render_to_pdf
import simplejson
from ets.compress import compress_json


WFP_ORGANIZATION = 'WFP'
WFP_DISTRUIBUTION = 'WFP_DISTRIB'
def waybill_detail(request, waybill, template="waybill/detail.html", extra_context=None):
    """utility that shows waybill's details"""    
    
    waybill_log = ets.models.ETSLogEntry.objects.filter(content_type__id=ContentType.objects.get_for_model(ets.models.Waybill).pk, object_id=waybill.pk)

    context = {
        'object': waybill,
        'items': waybill.loading_details.select_related(),
        'waybill_history': waybill_log,
    }
    apply_extra_context(extra_context or {}, context)
    return direct_to_template(request, template, context)


@waybill_user_related
def waybill_view(request, waybill_pk, queryset, template):
    """Waybill details view"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    return waybill_detail(request, waybill, template)
    

@waybill_user_related
def waybill_pdf(request, waybill_pk, queryset, template, print_original=False):
    """Generates PDF version of waybill"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    return render_to_pdf(request, template, {
                'print_original': print_original,
                'object': waybill,
                'items': waybill.loading_details.select_related(),
    }, 'waybill-%s' % waybill.pk)


@require_POST
@person_required
@dispatch_view
@transaction.commit_on_success
def waybill_finalize_dispatch(request, waybill_pk, template_name, queryset):
    """
    called when user pushes Print Original on dispatch
    Redirects to order details
    """

    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.dispatch_sign()
    create_logentry(request, waybill, log_models.CHANGE, "Signed dispatch waybill")
    
    return render_to_pdf(request, template_name, {
                'print_original': True,
                'object': waybill,
                'items': waybill.loading_details.select_related(),
    }, 'waybill-%s' % waybill.pk)
    

@require_POST
@person_required
@receipt_view
@transaction.commit_on_success
def waybill_finalize_receipt(request, waybill_pk, template_name, queryset):
    """ Signs reception"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt_sign()
    create_logentry(request, waybill, log_models.CHANGE, "Signed receive waybill")
    
    return render_to_pdf(request, template_name, {
                'print_original': True,
                'object': waybill,
                'items': waybill.loading_details.select_related(),
    }, 'waybill-%s' % waybill.pk)



@waybill_user_related
def waybill_list(request, queryset, template='waybill/list2.html', extra_context=None):
    """Shows waybill listing"""
    context = {'object_list': queryset.values(
        'order',
        'order__pk',
        'pk',
        'order__warehouse__location__name',
        'order__warehouse__name',
        'order__consignee__name',
        'order__location__name',
        'transport_dispach_signed_date',
        'receipt_signed_date',
        'validated',
        'receipt_validated',
        'sent_compas',
        'receipt_sent_compas',
        'destination__name',
        'transaction_type'
    ),}
    apply_extra_context(extra_context or {}, context)
    return direct_to_template(request, template, context)


def waybill_search( request, queryset, form_class=WaybillSearchForm, template='waybill/list2.html'):
    """Waybill search view. Simply a wrapper on waybill_list"""
    
    form = form_class(request.GET or None)
    search_string = form.cleaned_data['q'] if form.is_valid() else ''
    queryset = queryset.filter(pk__icontains=search_string)
    
    return waybill_list(request, queryset=queryset)


@transaction.commit_on_success
def _dispatching(request, waybill, template, success_message, created=False, form_class=DispatchWaybillForm, 
                formset_form=LoadingDetailDispatchForm, formset_class=BaseLoadingDetailFormSet):
    """Private function with common functionality for creating and editing dispatching waybill"""
    order = waybill.order
    
    class FormsetForm(formset_form):
        stock_item = forms.ModelChoiceField(queryset=order.get_stock_items(), label=_('Stock Item'), 
                                            empty_label=_("Choose stock item"))
        stock_item.choices = [(u"", stock_item.empty_label),]
        stock_item.choices+=[(item.pk, u"%s  - %s(kg)" % (unicode(item), item.unit_weight_net ))  
                             for item in order.get_stock_items().exclude(quantity_net=0)]
    
    loading_formset = inlineformset_factory(ets.models.Waybill, ets.models.LoadingDetail, 
                       form=FormsetForm, formset=formset_class, 
                       extra=1, max_num=5,
                       can_order=False, can_delete=True)\
        (request.POST or None, request.FILES or None, prefix='item', instance=waybill)
    
    form = form_class(data=request.POST or None, files=request.FILES or None, instance=waybill)
    
    #Filter choices
    #Warehouse
    warehouses = ets.models.Warehouse.get_warehouses(order.location, order.consignee).exclude(pk=order.warehouse.pk)
    
    form.fields['destination'].queryset = warehouses
    form.fields['destination'].empty_label = None
    
    #Transaction type
    if order.consignee.pk == WFP_ORGANIZATION:
        form.fields['transaction_type'].choices = ((k, v) for k, v in form.fields['transaction_type'].choices 
                                if (k ==ets.models.Waybill.INTERNAL_TRANSFER) or (k ==ets.models.Waybill.SHUNTING))
    if order.consignee.pk == WFP_DISTRUIBUTION:
        form.fields['transaction_type'].choices = ((k, v) for k, v in form.fields['transaction_type'].choices 
                                                   if k ==ets.models.Waybill.DISTIBRUTION)
    if not order.consignee.pk == WFP_DISTRUIBUTION:
        if not order.consignee.pk == WFP_ORGANIZATION:
            form.fields['transaction_type'].choices = ((k, v) for k, v in form.fields['transaction_type'].choices 
                                                       if k ==ets.models.Waybill.DELIVERY)
    
    if form.is_valid() and loading_formset.is_valid():
        waybill = form.save()
        loading_formset.save()
        
        if created:
            create_logentry(request, waybill, log_models.ADDITION, "Created dispatch waybill")
        else:
            create_logentry(request, waybill, log_models.CHANGE, ": ".join(["Edited dispatch waybill", construct_change_message(request, form, [loading_formset])]))
        
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
@transaction.commit_on_success
def waybill_create(request, order_pk, queryset, **kwargs):
    """Creates a Waybill"""
    
    order = get_object_or_404(queryset, pk=order_pk)
    waybill = ets.models.Waybill(order=order, dispatcher_person=request.user.person)

    return _dispatching(request, waybill, success_message=_("eWaybill has been created"), created=True,  **kwargs)


@person_required
@dispatch_view
@transaction.commit_on_success
def waybill_dispatch_edit(request, order_pk, waybill_pk, queryset, **kwargs):
    """Updates not signed dispatching waybill"""
    
    waybill = get_object_or_404(queryset, pk=waybill_pk, order__pk=order_pk)

    return _dispatching(request, waybill, success_message=_("eWaybill has been updated"), **kwargs) 


@transaction.commit_on_success
def waybill_reception(request, waybill_pk, queryset, form_class=WaybillRecieptForm, 
                      formset_form = LoadingDetailReceiptForm,
                      template='waybill/receive.html'):
    """Waybill reception view""" 
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
    form.fields['destination'].empty_label = None
    
    if form.is_valid() and loading_formset.is_valid():
        waybill = form.save()
        loading_formset.save()
        create_logentry(request, waybill, log_models.CHANGE, ": ".join(["Edited receive waybill", construct_change_message(request, form, [loading_formset])]))
        
        messages.add_message(request, messages.INFO, _('eWaybill has been discharged'))
        
        return redirect(waybill)
    
    return direct_to_template(request, template, {
        'form': form, 
        'formset': loading_formset,
        'waybill': waybill,
    })


@person_required
def waybill_reception_scanned(request, scanned_code, queryset):
    """Special view that accepts scanned data^ deserialized and redirect to waybill_receiption of that waybill"""
    waybill = ets.models.Waybill.decompress(scanned_code)

    if not waybill:
        raise Http404
    return waybill_reception(request, waybill.pk, queryset)


@require_POST
@person_required
@dispatch_view
@transaction.commit_on_success
def waybill_delete(request, waybill_pk, queryset, redirect_to=''):
    """Deletes specific waybill"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    create_logentry(request, waybill, log_models.DELETION)
    waybill.delete()
    redirect_to = redirect_to or request.GET.get('redirect_to', '')
        
    messages.info(request, _('eWaybill %(number)s has now been Removed') % {"number": waybill.pk})

    if redirect_to:
        return redirect(redirect_to)
    elif request.META.has_key('HTTP_REFERER'):
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')
        

@officer_required
@dispatch_compas
def dispatch_validates(request, queryset, template):
    """
    Listing of dispatch waybills. 
    Firstly officer validates a waybill, then he can push it to COMPAS. 
    Otherwise system does it every 2 minutes.
    """
    return direct_to_template(request, template, {
        'object_list': queryset.filter(validated=False),
        'validated_waybills': queryset.filter(validated=True),
        'logger_action': ets.models.CompasLogger.DISPATCH,
    })

@officer_required
@receipt_compas
def receipt_validates(request, queryset, template):
    """
    Listing of receipt waybills. 
    Firstly officer validates a waybill, then he can push it to COMPAS. 
    Otherwise system does it every 2 minutes.
    """
    return direct_to_template(request, template, {
        'object_list': queryset.filter(receipt_validated=False),
        'validated_waybills': queryset.filter(receipt_validated=True),
        'logger_action': ets.models.CompasLogger.RECEIPT,
    })


@require_POST
@officer_required
@dispatch_compas
@transaction.commit_on_success
def validate_dispatch(request, waybill_pk, queryset):
    """Sets dispatch 'validated' flag. It allows system to submit this waybill to COMPAS."""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.validated = True
    waybill.save()
    
    messages.add_message(request, messages.INFO, 
                        _('eWaybill %(waybill)s has been validated. It will be sent in few minutes.') % { 
                            'waybill': waybill.pk,
                        })

    return redirect('dispatch_validates')


@require_POST
@officer_required
@receipt_compas
@transaction.commit_on_success
def validate_receipt(request, waybill_pk, queryset):
    """Sets receipt 'validated' flag. It allows system to submit this waybill to COMPAS."""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt_validated = True
    waybill.save()
    
    messages.add_message(request, messages.INFO, 
                        _('eWaybill %(waybill)s has been validated. It will be sent in few minutes.') % { 
                            'waybill': waybill.pk,
                        })

    return redirect('receipt_validates')


def deserialize(request, form_class=WaybillScanForm):
    """
    View that accepts POST request with serialized and compress data. 
    And, decompress it, finds a waybill and redirects to waybill details.
    """
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
    """Bar code generator. This view uses 'pyqrcode' for back-end. It returns image file in response."""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    
    barcode = waybill.barcode_qr()
    return HttpResponse(barcode.read(), content_type="image/jpeg")
barcode_qr.authentication = False


def stock_items(request, template_name, queryset):
    """Listing of stock items splitted by warehouses."""
    if not request.user.has_perm("ets.stockitem_api_full_access"):
        queryset = queryset.filter(Q(persons__pk=request.user.pk) | Q(compas__officers=request.user))
    return object_list(request, queryset, paginate_by=5, template_name=template_name)


def get_stock_data(request, order_pk, queryset):
    """Utility ajax view that returns stock item information to fill dispatch form."""
    
    object_pk = request.GET.get('stock_item')
    
    if not request.user.has_perm("ets.stockitem_api_full_access"):
        queryset = queryset.filter(Q(warehouse__persons__pk=request.user.pk) | Q(warehouse__compas__officers=request.user))
    
    stock_item = get_object_or_404(queryset, pk=object_pk)
    
    return HttpResponse(simplejson.dumps({
        'unit_weight_net': stock_item.unit_weight_net,
        'unit_weight_gross': stock_item.unit_weight_gross,
        'number_of_units': min(stock_item.number_of_units, stock_item.get_order_quantity(order_pk)),
    }, use_decimal=True))

def sync_compas(request, queryset, template_name="sync/sync_compas.html"):
    """Landing page, that shows all COMPAS stations with possibility to import one-by-one."""
    
    if not request.user.is_superuser:
        queryset = queryset.filter(Q(warehouses__persons__pk=request.user.pk) | Q(officers=request.user))
        
    queryset = queryset.annotate(last_updated=Max('warehouses__stock_items__updated'))
    
    return direct_to_template(request, template=template_name, extra_context={'stations': queryset})


@require_POST
def handle_sync_compas(request, compas_pk, queryset):
    """Executes COMPAS import for specific station."""
    
    if not request.user.is_superuser:
        queryset = queryset.filter(officers=request.user)
        
    station = get_object_or_404(queryset, pk=compas_pk)
    
    #Execute external command
    Popen(['./bin/instance', 'sync_compas', '--compas=%s' % station.pk], cwd=settings.EGG_ROOT)
    
    messages.add_message(request, messages.INFO, 
                         _('Import process from %(station)s has been initiated. It might take several minutes.') % {
        "station": station.pk
    })
    
    return redirect('sync_compas')

    
@officer_required
@dispatch_compas
@transaction.commit_on_success
def send_dispatched_view(request, queryset):
    """Submits dispatch waybills to COMPAS"""
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
@transaction.commit_on_success
def send_received_view(request, queryset):
    """Submits received waybills to COMPAS"""
    for waybill in queryset:
        send_received(waybill)
    
    return redirect('receipt_validates')


def export_compas_file(request, compas=None, warehouse=None, data_type="json"):
    """Returns a file with all COMPAS data in response"""
    template = 'ets_data-%s' % ("compress" if data_type=="data" else data_type,)
    if compas:
        compas = get_object_or_404(ets.models.Compas, pk=compas)
        template = "-".join([template, compas.pk])
    if warehouse:
        warehouse = get_object_or_404(ets.models.Warehouse, pk=warehouse)
        template = "-".join([template, warehouse.pk])

    data = serializers.serialize('json', get_compas_data(compas=compas, warehouse=warehouse), use_decimal=False)
    template = "-".join([template, "%s"])

    if data_type == "data":
        data = compress_json(data)
        
    return data_to_file_response(data, file_name=template % datetime.date.today(), type=data_type)

    

class ImportData(FormView):
    """Imports file with compressed data, i.e. all datas from compas or eveb waybills"""
    template_name = 'sync/import_file.html'
    form_class = ImportDataForm
    
    def form_valid(self, form):
        _file = form.cleaned_data['file']

        total = import_file(_file)
        
        messages.add_message(self.request, messages.INFO, 
                             _('File has been imported successfully. Totally saved objects --> %s' % total))
        
        return self.get(self.request)

@officer_required
def installation_data(request, template_name="stock/warehouse_list.html",
                      queryset=ets.models.Warehouse.objects.all().order_by("compas__code", "code")):
    
    user = request.user
    compas_stations = user.compases.all().values_list('code')
    if not user.is_superuser:
        queryset.filter(compas__in=compas_stations)
    queryset.order_by("compas", "name")
    
    return object_list(request, queryset, paginate_by=settings.PAGINATION_DEFAULT_PAGINATION, template_name=template_name)
