import datetime
from functools import wraps

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.core import serializers
#from django.core.urlresolvers import reverse
#from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
#from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
#from django.utils import simplejson
from django.views.generic.simple import direct_to_template
#from django.views.generic.list_detail import object_list
#from django.views.generic.create_update import apply_extra_context
from django.contrib import messages
from django.db import transaction
#from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

#from uni_form.helpers import FormHelper, Layout, HTML, Row

#from ets.compas import compas_write
from ets.forms import WaybillRecieptForm, BaseLoadingDetailFormSet, DispatchWaybillForm
from ets.forms import WaybillSearchForm, LoadingDetailDispatchForm #, WaybillValidationFormset 
from ets.forms import LoadingDetailRecieptForm, BaseRecieptFormFormSet
from .decorators import person_required, officer_required, dispatch_view, receipt_view, waybill_user_related
import ets.models


@login_required
@waybill_user_related
def waybill_view(request, waybill_pk, queryset, template):
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    
    items = waybill.loading_details.select_related()
    items_count = len(items)
    
    return direct_to_template(request, template, {
        'object': waybill,
        'extra_lines': [''] * (settings.LOADING_LINES - items_count),
        'items': items,
        'items_count': items_count,
    })

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
    

@login_required
@person_required
@transaction.commit_on_success
def waybill_create(request, order_pk, form_class=DispatchWaybillForm, 
                   formset_form=LoadingDetailDispatchForm,
                   formset_class=BaseLoadingDetailFormSet,
                   order_queryset=ets.models.Order.objects.all(),
                   template='waybill/create.html' ):
    """Creates a Waybill"""
    
    order = get_object_or_404(order_queryset, pk=order_pk, warehouse__in=ets.models.Warehouse.filter_by_user(request.user)) 

    class FormsetForm(formset_form):
        stock_item = forms.ModelChoiceField(queryset=order.get_stock_items(), label=_('Stock Item'))
        
        #===============================================================================================================
        # def clean( self ):
        #    try:
        #        cleaned = self.cleaned_data
        #        stock_item = cleaned.get("stock_item")
        #        units = cleaned.get( "number_of_units" )
        #        overloaded = cleaned.get('overloaded_units')
        #        max_items = order_item.lti_line.items_left
        #        if units > max_items + self.instance.numberUnitsLoaded and  overloaded == False: #and not overloaded:
        #            myerror = "Overloaded!"
        #            self._errors['numberUnitsLoaded'] = self._errors.get( 'numberUnitsLoaded', [] )
        #            self._errors['numberUnitsLoaded'].append( myerror )
        #            raise forms.ValidationError( myerror )
        #        return cleaned
        #    except:
        #            myerror = "Value error!"
        #            self._errors['numberUnitsLoaded'] = self._errors.get( 'numberUnitsLoaded', [] )
        #            self._errors['numberUnitsLoaded'].append( myerror )
        #            raise forms.ValidationError( myerror )
        #===============================================================================================================          
    
    loading_formset = modelformset_factory(ets.models.LoadingDetail, 
                       form=FormsetForm,
                       formset = type('LoadingFormSet', (formset_class, forms.models.BaseModelFormSet), {}), 
                       extra=5, max_num=5,
                       can_order=False, can_delete=False)\
        (request.POST or None, request.FILES or None, prefix='item', queryset=ets.models.LoadingDetail.objects.none())
    
    form = form_class(data=request.POST or None, files=request.FILES or None, initial={
        'loading_date': order.dispatch_date,
        'dispatch_date': order.dispatch_date,
    })
    
    form.fields['destination'].queryset = ets.models.Warehouse.get_warehouses(order.location, order.consignee)\
                                                              .exclude(pk=order.warehouse.pk)
    
    if form.is_valid() and loading_formset.is_valid():
        waybill = form.save(False)
        waybill.order = order
        waybill.dispatcher_person = request.user.person
        waybill.save()
        
        for details in loading_formset.save(False):
            details.waybill = waybill
            details.save()
        
        messages.success(request, _("Waybill has been created."))
        return redirect(waybill)
        
    return direct_to_template( request, template, {
        'form': form, 
        'formset': loading_formset,
        'object': order,
    })


@login_required
@person_required
@dispatch_view
@transaction.commit_on_success
def waybill_dispatch_edit(request, order_pk, waybill_pk, queryset, form_class=DispatchWaybillForm, 
                          formset_form=LoadingDetailDispatchForm, formset_class=BaseLoadingDetailFormSet,
                          template='waybill/edit.html'):
    """Edit not signed dispatching waybill"""
    
    waybill = get_object_or_404(queryset, pk=waybill_pk, order__pk=order_pk)
    
    order = waybill.order
    
    class FormsetForm(formset_form):
        stock_item = forms.ModelChoiceField(queryset=order.get_stock_items(), label=_('Stock Item'))
        
    loading_formset = inlineformset_factory(ets.models.Waybill, ets.models.LoadingDetail, 
                       form=FormsetForm,
                       formset = type('DispatchLoadingFormSet', (formset_class, forms.models.BaseInlineFormSet), {}), 
                       extra=5, max_num=5,
                       can_order=False, can_delete=False)\
            (request.POST or None, request.FILES or None, instance=waybill, prefix='item')
    
    form = form_class(data=request.POST or None, files=request.FILES or None, instance=waybill)
    
    form.fields['destination'].queryset = ets.models.Warehouse.get_warehouses(order.location, order.consignee)\
                                                              .exclude(pk=order.warehouse.pk)
    
    if form.is_valid() and loading_formset.is_valid():
        form.save()
        loading_formset.save()
        
        messages.success(request, _("Waybill has been updated."))
        return redirect(waybill)
        
    return direct_to_template(request, template, {
        'form': form, 
        'formset': loading_formset,
        'object': order,
        'waybill': waybill,
    })
    


@login_required
@person_required
@receipt_view
def waybill_finalize_receipt(request, waybill_pk, queryset):
    """ Signs reception"""
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt.sign()
    
    messages.add_message( request, messages.INFO, _('Waybill %(waybill)s Receipt Signed') % { 
        'waybill': waybill.pk,
    })

    return redirect(waybill)


@login_required
@person_required
@receipt_view
@transaction.commit_on_success
def waybill_reception(request, waybill_pk, queryset, form_class=WaybillRecieptForm, 
                      formset_form = LoadingDetailRecieptForm,
                      formset_class = BaseRecieptFormFormSet,
                      template='waybill/receive.html'):
    
    waybill = get_object_or_404(queryset, pk=waybill_pk)
    
    loading_formset = inlineformset_factory(ets.models.Waybill, ets.models.LoadingDetail, 
                                            form=formset_form, extra=0, max_num=5,
                                            can_order=False, can_delete=False)\
                                (request.POST or None, request.FILES or None, instance=waybill, prefix='item')
    
    today = datetime.date.today()
    form = form_class(data=request.POST or None, files=request.FILES or None, initial = {
        'arrival_date': today,
        'start_discharge_date': today,
        'end_discharge_date': today,
    }, instance=waybill.get_receipt())
    
    if form.is_valid() and loading_formset.is_valid():
        receipt = form.save(False)
        receipt.waybill = waybill
        receipt.person = request.user.person
        receipt.save()
        
        loading_formset.save(True)
        
        return redirect(waybill)
    
    return direct_to_template(request, template, {
        'form': form, 
        'formset': loading_formset,
        'waybill': waybill,
    })


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
def waybill_validate(request, queryset, template, formset_model=ets.models.Waybill):
    
    formset = modelformset_factory(formset_model, fields = ('validated',), extra=0)\
                    (request.POST or None, request.FILES or None, queryset=queryset.filter(validated=False))
                                  
    if formset.is_valid():
        formset.save(commit=True)
        
        return redirect(request.build_absolute_uri())
    
    return direct_to_template(request, template, {
        'formset': formset, 
        'validated_waybills': queryset.filter(validated=True),
    })

@login_required
@officer_required
def dispatch_validate(request, queryset, **kwargs):
    return waybill_validate(request, queryset=queryset.filter(order__warehouse__compas__officers=request.user), **kwargs)

@login_required
@officer_required
def receipt_validate(request, queryset, **kwargs):
    return waybill_validate(request, queryset=queryset.filter(waybill__destination__compas__officers=request.user), **kwargs)

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
