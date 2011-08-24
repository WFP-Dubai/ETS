
import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory, model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import apply_extra_context
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


from uni_form.helpers import FormHelper, Layout, HTML, Row

from ets.compas import compas_write
from ets.forms import WaybillFullForm, WaybillRecieptForm, BaseLoadingDetailFormFormSet, DispatchWaybillForm
from ets.forms import WaybillValidationFormset, WaybillSearchForm, LoadingDetailDispatchForm
from ets.forms import LoadingDetailRecieptForm, BaseRecieptFormFormSet
import ets.models
from ets.tools import un64unZip, viewLog, default_json_dump

LOADING_LINES = 5


def prep_req( request ):

    return {'user': request.user}

def superuser_required(function=None, **kwargs):
    actual_decorator = user_passes_test(lambda u: u.is_superuser, **kwargs)
    if function:
        return actual_decorator(function)
    return actual_decorator

def officer_required(function=None, **kwargs):
    actual_decorator = user_passes_test(lambda u: u.get_profile().officer, **kwargs)
    if function:
        return actual_decorator(function)
    return actual_decorator


@login_required
def order_list(request, warehouse_pk=None, template='order/list.html', 
               queryset=ets.models.Order.objects.all().order_by('-created'), 
               extra_context=None):
    """
    URL: /orders/
    Shows all orders

    URL: /orders/{{ warehouse }}/
    Shows the orders that are in a specific warehouse
    """
    
    if warehouse_pk:
        queryset = queryset.filter(warehouse__pk=warehouse_pk)
        
    #TODO: Exclude delivered orders
    #===================================================================================================================
    # still_ltis = []
    # for lti in ltis:
    #    for si in LtiOriginal.objects.filter( code = lti['code'] ):
    #        if si.items_left > 0 and lti not in still_ltis:
    #            still_ltis.append( lti )
    #===================================================================================================================
    
    extra = {
        'warehouse_pk': warehouse_pk,
    }
    apply_extra_context(extra_context or {}, extra)
    
    return object_list(request, queryset=queryset, template_name=template, extra_context=extra)

@login_required
def waybill_view(request, waybill_pk, queryset, template):
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    my_empty = [''] * (LOADING_LINES - waybill.loading_details.count())
    
    return direct_to_template( request, template, {
        'object': waybill,
        'extra_lines': my_empty,
        'items': waybill.loading_details.select_related(),
        'items_count': waybill.loading_details.count(),
        'editable': waybill.is_editable(request.user),
    })

@login_required
def waybill_finalize_dispatch( request, waybill_pk, queryset):
    """
    called when user pushes Print Original on dispatch
    Redirects to order details
    """
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.dispatch_sign(True)
    
    messages.add_message( request, messages.INFO, _('Waybill %(waybill)s Dispatch Signed') % {
        "waybill": waybill.pk
    })
    
    return redirect( "order_detail", waybill.order_code)


@login_required
def waybill_search( request, form_class=WaybillSearchForm, 
                    queryset=ets.models.Waybill.objects.all(), template='waybill/list.html'):
#                    param_name='wbnumber', consegnee_code='W200000475' ):

    form = form_class(request.POST or None)
    search_string = form.cleaned_data['q'] if form.is_valid() else ''
    queryset = queryset.filter(pk__icontains=search_string)
    
    return direct_to_template( request, template, {
        'object_list': queryset, 
        'user': request.user,
    })


@login_required
@transaction.commit_on_success
def waybill_create_or_update(request, order_pk, form_class=DispatchWaybillForm, 
                             formset_form=LoadingDetailDispatchForm,
                             formset_class=BaseLoadingDetailFormFormSet,
                             order_queryset=ets.models.Order.objects.all(),
                             waybill_pk=None, waybill_queryset = ets.models.Waybill.objects.all(), 
                             template='waybill/create.html' ):
    """Creates a Waybill"""
    
    waybill = get_object_or_404(waybill_queryset, pk=waybill_pk, order_code=order_pk) if waybill_pk else None
    
    order = get_object_or_404(order_queryset, pk=order_pk)
    
    class FormsetForm( formset_form ):
        stock_item = forms.ModelChoiceField(queryset=order.get_stock_items(), label=_('Commodity'))
        
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
                                           formset = formset_class, 
                                           extra=5, max_num=5,
                                           can_order=False, can_delete=False)\
                                (request.POST or None, request.FILES or None, prefix='item')
    
    form = form_class(data=request.POST or None, files=request.FILES or None, instance=waybill, initial={
        'loading_date': order.dispatch_date,
        'dispatch_date': order.dispatch_date,
    })
    
    form.fields['destination'].queryset = ets.models.Warehouse.get_warehouses(order.location, order.consignee)\
                                                              .exclude(pk=order.warehouse.pk)
    
    if form.is_valid() and loading_formset.is_valid():
        waybill = form.save(False)
        waybill.order_code = order.pk
        waybill.project_number = order.project_number
        waybill.transport_name = order.transport_name
        waybill.warehouse = order.warehouse
        waybill.dispatcher_person = request.user.get_profile().compas_person
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
        'waybill': waybill,
        'user': request.user,
    })


@login_required
def waybill_finalize_receipt( request, waybill_pk, queryset):
    """
    View: waybill_finalize_receipt 
    URL:/waybill/receipt/
    Template:None
    Redirects to Lti Details
    Called when user pushes Print Original on Receipt
    """
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.receipt_sign()
    
    messages.add_message( request, messages.INFO, _('Waybill %(waybill)s Receipt Signed') % { 
        'waybill': waybill.pk,
    })

    return redirect( "waybill_reception_list" )

@login_required
def waybill_reception(request, waybill_pk, queryset, form_class=WaybillRecieptForm, 
                      formset_form = LoadingDetailRecieptForm,
                      formset_class = BaseRecieptFormFormSet,
                      template='waybill/receive.html'):
    
    waybill = get_object_or_404(queryset, pk=waybill_pk)
    
    today = datetime.date.today()
    
    
    loading_formset = inlineformset_factory(ets.models.Waybill, ets.models.LoadingDetail, 
                                            form=formset_form, formset=formset_class, 
                                            extra=0, max_num=5,
                                            can_order=False, can_delete=False)\
                                (request.POST or None, request.FILES or None, instance=waybill, prefix='item')
    
    form = form_class(data=request.POST or None, files=request.FILES or None, initial = {
        'arrival_date': today,
        'start_discharge_date': today,
        'end_discharge_date': today,
    }, instance=waybill.get_receipt())
    
    if form.is_valid() and loading_formset.is_valid():
        receipt = form.save(False)
        receipt.waybill = waybill
        receipt.person = request.user.get_profile().compas_person
        receipt.save()
        
        loading_formset.save(True)
        
        return redirect(waybill)
    
    return direct_to_template(request, template, {
        'form': form, 
        'formset': loading_formset,
        'waybill': waybill,
        'user': request.user,
    })


#=======================================================================================================================
# 
# def create_or_update(waybill, user, error_message):
#    compas_logger, created = CompasLogger.objects.get_or_create(wb = waybill, defaults={
#        "user": user, 
#        "errorDisp": error_message, 
#        "timestamp": datetime.datetime.now()
#    })
#    
#    if not created:
#        compas_logger.user = user
#        compas_logger.errorDisp = error_message
#        compas_logger.timestamp = datetime.datetime.now()
#        compas_logger.save()
#    
#    return compas_logger
# 
# @login_required
# def singleWBDispatchToCompas( request, waybill_pk, queryset=ets.models.Waybill.objects.all() ):
#    """
#    View: singleWBDispatchToCompas
#    URL: 
#    
#    Sends a single Dipatch into compas
#    """
#    waybill = get_object_or_404(queryset, pk = waybill_pk )
#    the_compas = compas_write()
#    error_message, error_codes = '', ''
#    if the_compas.write_dispatch_waybill_compas( waybill_pk ):
#        CompasLogger.objects.filter( wb = waybill ).delete()
#        
#        waybill.waybillSentToCompas = True
#        waybill.save()
#        
#        messages.add_message( request, messages.INFO, 
#                _('Waybill %(waybill)s Sucsessfully pushed to COMPAS') % {'waybill': waybill.waybillNumber} )
#    else:
#        create_or_update(waybill, request.user, the_compas.ErrorMessages)
# 
#        waybill.waybillValidated = False
#        waybill.save()
#        messages.add_message( request, messages.ERROR, 
#                              _('Problem sending to compas: %(message)s') % { 'message': the_compas.ErrorMessages} )
#        
#        error_message += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorMessages)
#        error_codes += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorCodes)
#        
#    # Update stock after submit off waybill
#    EpicStock.update()
#    
#    return redirect("waybill_validate_dispatch_form")
# 
# 
# @login_required
# def singleWBReceiptToCompas( request, waybill_pk, queryset=ets.models.Waybill.objects.all(), template='compas/status_waybill_compas_rec.html' ):
#    """
#    View: singleWBReceiptToCompas
#    URL: ...
#    Template: //waybill/templates/compas/status_waybill_compas_rec.html
#    Sends a single Receipt into compas
#    """
#    #profile = getMyProfile(request)
#    waybill = get_object_or_404(queryset, pk = waybill_pk )
#    the_compas = compas_write()
#    error_message, error_codes = '', ''
#    if  the_compas.write_receipt_waybill_compas( waybill.pk ):
#        CompasLogger.objects.filter( wb = waybill ).delete()
# 
#        waybill.waybillRecSentToCompas = True
#        waybill.save()
#    else:
#        create_or_update(waybill, request.user, the_compas.ErrorMessages)
#        
#        waybill.waybillReceiptValidated = False
#        waybill.save()
#        
#        error_message += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorMessages)
#        error_codes += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorCodes)
#    
#    # add field to say compas error/add logging Change to use messages....
#    return direct_to_template( request,template, {
#        'waybill': waybill,
#        'error_message': error_message,
#        'error_codes': error_codes,
#    })
# 
# 
# @login_required
# def receiptToCompas( request, template='compas/list_waybills_compas_received.html' ):
# 
#    list_waybills = Waybill.objects.filter(waybillReceiptValidated = True, 
#                                           waybillRecSentToCompas = False, 
#                                           waybillSentToCompas = True )
#    the_compas = compas_write()
#    error_message, error_codes = '', ''
#    
#    for waybill in list_waybills:
#        # call compas and read return
#        if the_compas.write_receipt_waybill_compas( waybill.pk ):
#            waybill.waybillRecSentToCompas = True
#            waybill.save()
#        else:
#            error_message += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorMessages)
#            error_codes += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorCodes)
#    
#    return direct_to_template( request,template, {
#        'waybill_list': list_waybills, 
#        'error_message': error_message, 
#        'error_codes': error_codes,
#    })
#=======================================================================================================================

@login_required
def waybill_delete(request, waybill_pk, redirect_to='', queryset=ets.models.Waybill.objects.all()):
    waybill = get_object_or_404(queryset, pk = waybill_pk)
    waybill.delete()
    messages.info(request, _('Waybill %(number)s has now been Removed') % {"number": waybill.pk})
    if redirect_to:
        return redirect(redirect_to)
    else:
        return redirect(request.META['HTTP_REFERER'])
        

@login_required
def waybill_validate_form_update(request, waybill_pk, queryset, 
                                 template='waybill/waybill_detail.html'):
    """
    Admin Edit waybill
    waybill/validate/(.*)
    waybill/waybill_detail.html
    """
    current_wb = get_object_or_404(queryset, pk = waybill_pk)
    
    lti_code = current_wb.ltiNumber
    current_lti = LtiOriginal.objects.filter( code = lti_code )
    current_audit = current_wb.audit_log.all()
    current_wb.auditComment = ''
    current_items = LtiWithStock.objects.filter( lti_code = lti_code )
    myerror = current_wb.errors()

    if myerror:
        current_wb.dispError, current_wb.recError = myerror.errorDisp, myerror.errorRec
        
    class LRModelChoiceField( forms.ModelChoiceField ):
        def label_from_instance( self, obj ):
            cause = obj.cause
            length_c = len( cause ) - 10
            if length_c > 20:
                cause = "%s...%s" % (cause[0:20], cause[length_c:])
            return cause
    
    comm_cats = [item.comm_category_code for item in current_lti if item]
    
    class LoadingDetailDispatchForm( forms.ModelForm ):
        order_item = forms.ModelChoiceField( queryset = current_items, label = 'Commodity' )
        numberUnitsLoaded = forms.CharField(_("number of units loaded"), widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsGood = forms.CharField(_("number of units good"), widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsLost = forms.CharField(_("number of units lost"), widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsDamaged = forms.CharField(_("number of units damaged"), widget = forms.TextInput( attrs = {'size':'5'} ), required = False )

        unitsLostReason = LRModelChoiceField(label = _("units lost reason"), queryset = EpicLossDamages.objects.filter(type = 'L', comm_category_code__in = comm_cats ) , required = False )
        unitsDamagedReason = LRModelChoiceField(label = _("units damaged reason"), queryset = EpicLossDamages.objects.filter( type = 'D', comm_category_code__in = comm_cats ) , required = False )

        class Meta:
            model = LoadingDetail
            fields = ( 
                'wbNumber', 'order_item', 'numberUnitsLoaded', 'numberUnitsGood', 
                'numberUnitsLost', 'numberUnitsDamaged', 'unitsLostReason', 
                'unitsDamagedReason', 'unitsDamagedType', 'unitsLostType', 
                'overloadedUnits', 'overOffloadUnits' 
            )

    LDFormSet = inlineformset_factory( Waybill, LoadingDetail, LoadingDetailDispatchForm, 
                                       fk_name = "wbNumber", extra = 0 )
    
    qs = Place.objects.filter( geo_name = current_lti[0].destination_loc_name, 
                               organization_id = current_lti[0].consegnee_code )
    if len( qs ) == 0:
        qs = Place.objects.filter( geo_name = current_lti[0].destination_loc_name )

    if request.method == 'POST':
        form = WaybillFullForm( request.POST or None, instance = current_wb )
        form.fields["destinationWarehouse"].queryset = qs
        formset = LDFormSet( request.POST, instance = current_wb )
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect( "waybill_search" )
    else:
        form = WaybillFullForm( instance = current_wb )
        form.fields["destinationWarehouse"].queryset = qs

        formset = LDFormSet( instance = current_wb )
    
    return direct_to_template( request,template, {
        'form': form, 'lti_list': current_lti, 
        'formset': formset, 'audit': current_audit
    })


@login_required
@officer_required
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

## receives a POST with the compressed or uncompressed WB and sends you to the Receive WB
@login_required
@require_POST
def deserialize( request ):
    #TODO: rewrite in with a form
    waybillnumber = ''
    wb_data = request.POST['wbdata']
    wb_serialized = ''
    
    if wb_data[0] == '[':
        
        wb_serialized = wb_data
    else:   
        wb_serialized = un64unZip( wb_data )
        if wb_serialized is not None:
            wb_serialized = eval(wb_serialized)
        else:
            messages.error(request, _('Data Incorrect!!!'))
            return redirect(reverse('index')) 
 
    for obj in serializers.deserialize( "json", wb_serialized ):
        
        if type( obj.object ) is Waybill:
            waybillnumber = obj.object.pk
    
    return redirect(waybill_reception, waybillnumber )

def viewLogView( request, template='status.html' ):
    return direct_to_template( request, template, {'status': '<h3>Log view</h3><pre>%s</pre>' % viewLog()})

def expand_response(response, **headers):
    for header, value in headers.items():
        response[header] = value
    return response

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

@csrf_exempt
def post_synchronize_waybill( request ):
    '''
    This method is called by the offline application,
    that posts a serialized waybill.
    The waybill is deserialized and stored in the online database.
    '''
    if request.method == 'POST':
        serilized_waybill = request.POST['serilized_waybill']

        # change app_label
        serilized_waybill_str = str( serilized_waybill ).replace( '"offliner.', '"waybill.' )

        wb = None

        # try to deserialize waybill and loadingdetails and store in waybill online db
        is_an_update = False
        for obj in serializers.deserialize( "json", serilized_waybill_str ):
            #from waybill.models import Waybill, LoadingDetail
            if isinstance( obj.object, Waybill ):
                if Waybill.objects.filter( waybillNumber = obj.object.waybillNumber ).count() == 0:
                    # perform an insert
                    try:
                        obj.object.id = None
                        obj.object.save()
                        wb = obj.object
                    except:
                        print 'Exception when inserting Waybill'
                else:
                    is_an_update = True
                    # perform an update
                    try:
                        obj.object.id = Waybill.objects.filter( waybillNumber = obj.object.waybillNumber )[0].id
                        obj.object.save()
                        wb = obj.object
                    except:
                        print 'Exception when updating Waybill'

            elif isinstance( obj.object, LoadingDetail ) and wb is not None and not is_an_update:
                try:
                    obj.object.id = None
                    obj.object.wbNumber = wb
                    obj.object.save()
                except:
                    print 'Exception when saving LoadingDetail'
    response = HttpResponse( 'SYNCHRONIZATION_DONE' )
    return response

def get_wb_stock( request, queryset=ets.models.Warehouse.objects.all() ):
    warehouse = get_object_or_404(queryset, pk = request.REQUEST['warehouse'])
    filename = 'stock-data-%s-%s-%s.json' % (warehouse.origin_wh_code, settings.COMPAS_STATION, datetime.date.today())
    
    return expand_response(HttpResponse(warehouse.serialize(), content_type="application/json; charset=utf-8"),
                           **{'Content-Disposition': 'attachment; filename=' + filename})
    
    #===================================================================================================================
    # filename = 'stock-data-' + the_wh.origin_wh_code + '-' + settings.COMPAS_STATION + '-' + str( datetime.date.today() ) + '.json'
    # print filename
    # response = HttpResponse( mimetype = 'application/json' )
    # response['Content-Disposition'] = 'attachment; filename=' + filename
    # response.write( data )
    # return response
    #===================================================================================================================
    
#=======================================================================================================================
# @csrf_exempt
# def get_all_data( request ):
#    #print 'See'
#    return HttpResponse(serialized_all_items(), 
#                        content_type="application/json; charset=utf-8")
#=======================================================================================================================

#=======================================================================================================================
# @csrf_exempt
# def get_all_data_download( request ):
#    #print 'Donwload'
#    return expand_response(HttpResponse(serialized_all_items(), content_type='text/csv'),
#                           **{'Content-Disposition': 'attachment; filename=data-%s-%s.csv' % 
#                              (settings.COMPAS_STATION, datetime.date.today())})
#=======================================================================================================================
    
    #===================================================================================================================
    # data = serialized_all_items()
    # response = HttpResponse( mimetype = 'text/csv' )
    # response['Content-Disposition'] = 'attachment; filename=data-' + settings.COMPAS_STATION + '-' + str( datetime.date.today() ) + '.csv'
    # response.write( data )
    # return response
    #===================================================================================================================
