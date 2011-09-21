import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
#from django.core import serializers
from django.forms.models import inlineformset_factory
#from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.http import Http404
#from django.views.generic.list_detail import object_list
#from django.views.generic.create_update import apply_extra_context
from django.contrib import messages
from django.db import transaction
from django.utils.translation import ugettext as _

from ets.forms import WaybillRecieptForm, BaseLoadingDetailFormSet, DispatchWaybillForm
from ets.forms import WaybillSearchForm, LoadingDetailDispatchForm #, WaybillValidationFormset 
from ets.forms import LoadingDetailRecieptForm, WaybillScanForm
from .decorators import person_required, officer_required, dispatch_view, receipt_view, waybill_user_related 
from .decorators import warehouse_related, dispatch_compas, receipt_compas
import ets.models
from ets.utils import changed_fields, history_list


def waybill_detail(request, waybill, template="waybill/detail.html"):
    """utility that shows waybill's details"""    
    items = waybill.loading_details.select_related()
    items_count = len(items)
    
    return direct_to_template(request, template, {
        'object': waybill,
        'extra_lines': (),#[''] * (settings.LOADING_LINES - items_count),
        'items': items,
        'items_count': items_count,
    })


@login_required
@waybill_user_related
def waybill_view(request, waybill_pk, queryset, template):
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    return waybill_detail(request, waybill, template)
    

@login_required
@person_required
@dispatch_view
def waybill_finalize_dispatch( request, waybill_pk, queryset):
    """
    called when user pushes Print Original on dispatch
    Redirects to order details
    """
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.dispatch_sign(True)
    
    messages.add_message(request, messages.INFO, _('Waybill %(waybill)s Dispatch Signed') % {
        "waybill": waybill.pk
    })
    
    return redirect(waybill)


@login_required
@waybill_user_related
def waybill_list(request, queryset, template='waybill/list.html'):
    """Shows waybill listing"""
    return direct_to_template(request, template, {'object_list': queryset,})

@login_required
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
                       extra=5, max_num=5,
                       can_order=False, can_delete=False)\
        (request.POST or None, request.FILES or None, prefix='item', instance=waybill)
    
    form = form_class(data=request.POST or None, files=request.FILES or None, instance=waybill)
    
    form.fields['destination'].queryset = ets.models.Warehouse.get_warehouses(order.location, order.consignee)\
                                                              .exclude(pk=order.warehouse.pk)
    
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


@login_required
@person_required
@warehouse_related
def waybill_create(request, order_pk, queryset, **kwargs):
    """Creates a Waybill"""
    
    order = get_object_or_404(queryset, pk=order_pk)
    waybill = ets.models.Waybill(order=order, dispatcher_person = request.user.person,
                                 loading_date=order.dispatch_date, dispatch_date=order.dispatch_date)

    return _dispatching(request, waybill, success_message=_("Waybill has been created"), **kwargs)


@login_required
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
    
    form.fields['destination'].queryset = request.user.person.get_warehouses().exclude(pk=waybill.order.warehouse.pk)
    
    if form.is_valid() and loading_formset.is_valid():
        waybill = form.save()
        loading_formset.save()
        
        return redirect(waybill)
    
    return direct_to_template(request, template, {
        'form': form, 
        'formset': loading_formset,
        'waybill': waybill,
    })


@login_required
@person_required
@receipt_view
def waybill_finalize_receipt(request, waybill_pk, queryset):
    """ Signs reception"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt_sign()
    
    messages.add_message( request, messages.INFO, _('Waybill %(waybill)s Receipt Signed') % { 
        'waybill': waybill.pk,
    })

    return redirect(waybill)


@login_required
@person_required
def waybill_reception_scanned(request, scanned_code, queryset):
    waybill = ets.models.Waybill.decompress(scanned_code)
    if not waybill:
        raise Http404
    return waybill_reception(request, waybill.pk, queryset)


@login_required
@person_required
@dispatch_view
def waybill_delete(request, waybill_pk, queryset, redirect_to=''):
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.delete()
    
    messages.info(request, _('Waybill %(number)s has now been Removed') % {"number": waybill.pk})
    
    if redirect_to:
        return redirect(redirect_to)
    elif request.META.has_key('HTTP_REFERER'):
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('index')
        

@login_required
@officer_required
@dispatch_compas
def dispatch_validates(request, queryset, template):
    return direct_to_template(request, template, {
        'object_list': queryset.filter(validated=False),
        'validated_waybills': queryset.filter(validated=True),
    })

@login_required
@officer_required
@receipt_compas
def receipt_validates(request, queryset, template):
    return direct_to_template(request, template, {
        'object_list': queryset.filter(receipt_validated=False),
        'validated_waybills': queryset.filter(receipt_validated=True),
    })


@login_required
@officer_required
@dispatch_compas
def validate_dispatch(request, waybill_pk, queryset):
    """Sets 'validated' flag"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.validated = True
    waybill.save()
    
    messages.add_message( request, messages.INFO, _('Waybill %(waybill)s has been validated') % { 
        'waybill': waybill.pk,
    })

    return redirect('dispatch_validates')


@login_required
@officer_required
@receipt_compas
def validate_receipt(request, waybill_pk, queryset):
    """Sets 'validated' flag"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt.validated = True
    waybill.receipt.save()
    
    messages.add_message( request, messages.INFO, _('Waybill %(waybill)s has been validated') % { 
        'waybill': waybill.pk,
    })

    return redirect('receipt_validates')


@login_required
def deserialize(request, form_class=WaybillScanForm):
    form = form_class(request.GET or None)
    if form.is_valid():
        data = form.cleaned_data['data']
        waybill = ets.models.Waybill.decompress(data)
        if waybill:
            if request.GET.get("receipt",""):
                return redirect('waybill_reception_scanned', scanned_code=data )
            return waybill_detail(request, waybill)

    messages.error(request, _('Data Incorrect!!!'))
    return redirect('index')


def waybill_history(request, template, waybill_pk, loading_detail_queryset=ets.models.LoadingDetail.audit_log.all()):
    
    waybill = get_object_or_404(ets.models.Waybill, pk=waybill_pk)
    waybill_log = waybill.audit_log.all().order_by('-action_id')
    waybill_history = history_list(waybill_log, ets.models.Waybill)
            
    loading_detail_queryset = loading_detail_queryset.filter(waybill__pk=waybill_pk).order_by('-action_id')
    loading_detail_history = history_list(loading_detail_queryset, ets.models.LoadingDetail)
                
    return direct_to_template(request, template, {
        'waybill': waybill,
        'waybill_history': waybill_history,
        'loading_detail_history': loading_detail_history,       
    })
    

#=======================================================================================================================
# def barcode_qr( request, waybill_pk, queryset=Waybill.objects.all() ):
# #    import sys
# #    if sys.platform == 'darwin':
# #        from qrencode import Encoder
# #        enc = Encoder()
# #        myz = wb_compress( wb )
# #        im = enc.encode( myz, { 'width': 350 } )
# #        response = HttpResponse( mimetype = "image/png" )
# #        im.save( response, "PNG" )
# #    else:
#    
#    waybill = get_object_or_404(queryset, pk=waybill_pk)
# 
#    import subprocess
#    myz = waybill.compress()
#    print myz
#    mydata = subprocess.Popen( ['zint', '--directpng', '--barcode=58', '-d%s' % myz ], stdout = subprocess.PIPE )
#    image = mydata.communicate()[0]
#    #print mydata.communicate()
#    return HttpResponse( image, mimetype = "Image/png" )
#=======================================================================================================================

#=======================================================================================================================
# @csrf_exempt
# def post_synchronize_waybill( request ):
#    '''
#    This method is called by the offline application,
#    that posts a serialized waybill.
#    The waybill is deserialized and stored in the online database.
#    '''
#    if request.method == 'POST':
#        serilized_waybill = request.POST['serilized_waybill']
# 
#        # change app_label
#        serilized_waybill_str = str( serilized_waybill ).replace( '"offliner.', '"waybill.' )
# 
#        wb = None
# 
#        # try to deserialize waybill and loadingdetails and store in waybill online db
#        is_an_update = False
#        for obj in serializers.deserialize( "json", serilized_waybill_str ):
#            #from waybill.models import Waybill, LoadingDetail
#            if isinstance( obj.object, Waybill ):
#                if Waybill.objects.filter( waybillNumber = obj.object.waybillNumber ).count() == 0:
#                    # perform an insert
#                    try:
#                        obj.object.id = None
#                        obj.object.save()
#                        wb = obj.object
#                    except:
#                        print 'Exception when inserting Waybill'
#                else:
#                    is_an_update = True
#                    # perform an update
#                    try:
#                        obj.object.id = Waybill.objects.filter( waybillNumber = obj.object.waybillNumber )[0].id
#                        obj.object.save()
#                        wb = obj.object
#                    except:
#                        print 'Exception when updating Waybill'
# 
#            elif isinstance( obj.object, LoadingDetail ) and wb is not None and not is_an_update:
#                try:
#                    obj.object.id = None
#                    obj.object.wbNumber = wb
#                    obj.object.save()
#                except:
#                    print 'Exception when saving LoadingDetail'
#    response = HttpResponse( 'SYNCHRONIZATION_DONE' )
#    return response
#=======================================================================================================================
