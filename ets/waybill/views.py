
import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
#from django.core.urlresolvers import reverse
#from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory, modelformset_factory, ModelChoiceIterator, model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.views.generic.simple import direct_to_template
from django.contrib import messages

from ets.waybill.compas import compas_write
from ets.waybill.forms import WaybillFullForm, WaybillRecieptForm, BaseLoadingDetailFormFormSet, WaybillForm
from ets.waybill.forms import WaybillValidationFormset, WarehouseForm
from ets.waybill.models import LtiOriginal, RemovedLtis, Waybill, CompasLogger 
from ets.waybill.models import LtiWithStock, EpicLossDamages, LoadingDetail
from ets.waybill.models import Places, EpicPerson, EpicStock, DispatchPoint
from ets.waybill.tools import restant_si 
from ets.waybill.tools import import_setup, import_lti, track_compas_update
from ets.waybill.tools import un64unZip, viewLog 
from ets.waybill.tools import serialized_all_items
from django.utils.translation import ungettext as _


def prep_req( request ):

    return {'user': request.user}

@login_required
def select_action( request, **kwargs ):
    """
    View: select_action 
    URL: /ets/select-action
    Template: /ets/waybill/templates/select_action.html
    Gives the loggedin user a choise of possible actions sepending on roles
    """
    
    return direct_to_template(request, **kwargs)
    

@login_required
def listOfLtis( request, origin, template='lti/ltis.html'):
    """
    View: listOfLtis 
    URL: ets/waybill/list/{{warehouse}}
    Template: /ets/waybill/templates/ltis.html
    Shows the LTIs that are in a specific warehouse
    """
    
    if settings.DISABLE_EXPIERED_LTI:
        date_check = datetime.datetime.strptime( settings.MAX_DATE, '%Y-%m-%d' ).date()
    else:
        date_check = datetime.date.today()

    ltis = LtiOriginal.objects.values( 'code', 'destination_loc_name', 'consegnee_name', 'lti_date' , 'expiry_date' )\
                              .distinct().filter( expiry_date__gt = date_check, origin_wh_code = origin )

    still_ltis = []
    for lti in ltis:
        for item in restant_si( lti['code'] ):
            if item.CurrentAmount > 0 and lti not in still_ltis:
                still_ltis.append( lti )

    return direct_to_template(request, template, {'ltis': still_ltis})

## Show all ltis 
@login_required
def ltis( request, template='lti/ltis_all_qs.html' ):
    """
    View:
    ltis
    URL: ets/waybill/list
    Shows all the LTIs
    template:
    /ets/waybill/templates/ltis.html
    """
    if settings.DISABLE_EXPIERED_LTI:
        date_check = datetime.datetime.strptime( settings.MAX_DATE, '%Y-%m-%d' ).date()
    else:
        date_check = datetime.date.today()
    removedLtis = RemovedLtis.objects.all()
    
    ltis = LtiOriginal.objects.exclude( pk__in = removedLtis ).filter( expiry_date__gt = date_check )\
                              .values( 'code', 'destination_loc_name', 'consegnee_name', 'lti_date', 
                                       'requested_dispatch_date', 'origin_loc_name' , 'expiry_date' )\
                              .distinct().order_by( '-lti_date' )
    still_ltis = []
    for lti in ltis:
        for si in LtiOriginal.objects.filter( code = lti['code'] ):
            if si.items_left > 0 and lti not in still_ltis:
                still_ltis.append( lti )
    
    return direct_to_template(request, template , {'ltis': still_ltis})


def import_ltis( request ):
    """
    View: import_ltis 
    URL: ets/waybill/import
    Template: /ets/waybill/templates/status.html
    Executes Imports of LTIs, Persons, Stock, and updates SiTracker,
    add tag to say when last done
    """

    print 'Import Persons'
    EpicPerson.update()
    print 'Import GEO'
    Places.update()
    print 'Import Stock'
    EpicStock.update()
    print 'Import Setup'
    import_setup()
    print 'Import LTIs'
    import_lti()
    status = 'Import Finished'
    track_compas_update()
    messages.add_message( request, messages.INFO, status )

    return redirect("select_action")

def lti_detail_url( request, lti_code, template='lti/detailed_lti.html' ):
    """
    View: lti_detail_url 
    URL: ets/waybill/info/(lti_code)
    Template: /ets/waybill/templates/lti/detailed_lti.html
    Show detail of LTI and link to create waybill
    """
    detailed_lti = LtiOriginal.objects.filter( code = lti_code )
    listOfWaybills = Waybill.objects.filter( invalidated = False, ltiNumber = lti_code )
    listOfSI_withDeduction = restant_si( lti_code )
    
    lti_more_wb = False
    for item in detailed_lti:
        if item.items_left > 0:
            lti_more_wb = True
    
    return direct_to_template( template, {
        'detailed': detailed_lti, 
        'lti_id': lti_code, 
        'listOfWaybills': listOfWaybills, 
        'listOfSI_withDeduction': listOfSI_withDeduction, 
        'moreWBs':lti_more_wb
    })

@login_required
def dispatch( request ):
    """
    View: dispatch 
    URL: ets/waybill/dispatch
    Template: None
    Redirects to Lti Details.
    """
    try:
        return redirect( "listOfLtis", request.user.get_profile().warehouses.origin_wh_code )
    except:
        return redirect( "select_action" )

#### Waybill Views
#=======================================================================================================================
# @login_required
# def waybill_create( request, lti_pk, queryset=LtiOriginal.objects.all(), template='detailed_waybill.html' ):
#    try:
#        return direct_to_template( template, {
#            'detailed': queryset.get( lti_pk = lti_pk ), 
#            'lti_id': lti_pk,
#        })
#    except:
#        return redirect( "select_action" )
#=======================================================================================================================


@login_required
def waybill_finalize_dispatch( request, wb_id, queryset=Waybill.objects.all() ):
    """
    View: waybill_finalize_dispatch
    URL: ets/waybill/dispatch
    Templet:None
    called when user pushes Print Original on dispatch
    Redirects to Lti Details
    """
    current_wb = get_object_or_404(queryset, id = wb_id)

    current_wb.transportDispachSigned = True
    current_wb.transportDispachSignedTimestamp = datetime.datetime.now()
    current_wb.dispatcherSigned = True
    current_wb.auditComment = _('Print Dispatch Original')
    
    for lineitem in current_wb.loadingdetail_set.select_related():
        lineitem.order_item.lti_line.reduce_si( lineitem.numberUnitsLoaded )
    
    current_wb.save()
    messages.add_message( request, messages.INFO, _('Waybill')' %s'_(' Dispatch Signed') % current_wb.waybillNumber )
    
    return redirect( "lti_detail_url", current_wb.ltiNumber)


@login_required
def waybill_finalize_receipt( request, wb_id ):
    """
    View: waybill_finalize_receipt 
    URL:ets/waybill/receipt/
    Template:None
    Redirects to Lti Details
    Called when user pushes Print Original on Receipt
    """
    try:
        current_wb = Waybill.objects.get( id = wb_id )
        current_wb.recipientSigned = True
        current_wb.transportDeliverySignedTimestamp = datetime.datetime.now()
        current_wb.recipientSignedTimestamp = datetime.datetime.now()
        current_wb.transportDeliverySigned = True
        current_wb.auditComment = _('Print Dispatch Receipt')
        current_wb.save()
        
        messages.add_message( request, messages.INFO, _('Waybill')' %s'_('Receipt Signed') % current_wb.waybillNumber )
    except:
        pass
    
    return redirect( "waybill_reception_list" )


def create_or_update(waybill, user, error_message):
    compas_logger, created = CompasLogger.objects.get_or_create(wb = waybill, defaults={
        "user": user, 
        "errorDisp": error_message, 
        "timestamp": datetime.datetime.now()
    })
    
    if not created:
        compas_logger.user = user
        compas_logger.errorDisp = error_message
        compas_logger.timestamp = datetime.datetime.now()
        compas_logger.save()
    
    return compas_logger

@login_required
def singleWBDispatchToCompas( request, wb_id, queryset=Waybill.objects.all() ):
    """
    View: singleWBDispatchToCompas
    URL: 
    
    Sends a single Dipatch into compas
    """
    waybill = get_object_or_404(queryset, id = wb_id )
    the_compas = compas_write()
    error_message, error_codes = '', ''
    if the_compas.write_dispatch_waybill_compas( wb_id ):
        CompasLogger.objects.filter( wb = waybill ).delete()
        
        waybill.waybillSentToCompas = True
        waybill.save()
        
        messages.add_message( request, messages.INFO, 
                              _('Waybill')' %s' _('Sucsessfully pushed to COMPAS') % waybill.waybillNumber )
    else:
        create_or_update(waybill, request.user, the_compas.ErrorMessages)

        waybill.waybillValidated = False
        waybill.save()
        messages.add_message( request, messages.ERROR, _('Problem sending to compas:')' %s' % the_compas.ErrorMessages )
        
        error_message += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorMessages)
        error_codes += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorCodes)
        
    # Update stock after submit off waybill
    EpicStock.update()
    
    return redirect("waybill_validate_dispatch_form")


@login_required
def singleWBReceiptToCompas( request, wb_id, queryset=Waybill.objects.all(), template='compas/status_waybill_compas_rec.html' ):
    """
    View: singleWBReceiptToCompas
    URL: ...
    Template: /ets/waybill/templates/compas/status_waybill_compas_rec.html
    Sends a single Receipt into compas
    """
    #profile = getMyProfile(request)
    waybill = get_object_or_404(queryset, id = wb_id )
    the_compas = compas_write()
    error_message, error_codes = '', ''
    if  the_compas.write_receipt_waybill_compas( waybill.id ):
        CompasLogger.objects.filter( wb = waybill ).delete()

        waybill.waybillRecSentToCompas = True
        waybill.save()
    else:
        create_or_update(waybill, request.user, the_compas.ErrorMessages)
        
        waybill.waybillReceiptValidated = False
        waybill.save()
        
        error_message += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorMessages)
        error_codes += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorCodes)
    
    # add field to say compas error/add logging Change to use messages....
    return direct_to_template( template, {
        'waybill': waybill,
        'error_message': error_message,
        'error_codes': error_codes,
    })


@login_required
def receiptToCompas( request, template='compas/list_waybills_compas_received.html' ):

    list_waybills = Waybill.objects.filter( invalidated = False, waybillReceiptValidated = True, 
                                            waybillRecSentToCompas = False, waybillSentToCompas = True )
    the_compas = compas_write()
    error_message, error_codes = '', ''
    
    for waybill in list_waybills:
        # call compas and read return
        if the_compas.write_receipt_waybill_compas( waybill.id ):
            waybill.waybillRecSentToCompas = True
            waybill.save()
        else:
            error_message += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorMessages)
            error_codes += "%s-%s" % (waybill.waybillNumber, the_compas.ErrorCodes)
    
    return direct_to_template( template, {
        'waybill_list': list_waybills, 
        'error_message': error_message, 
        'error_codes': error_codes,
    })


def invalidate_waybill( request, wb_id, queryset=Waybill.objects.all(), template='status.html' ):
    #first mark waybill invalidate, then zero the stock usage for each line and update the si table
    current_wb = get_object_or_404(queryset, id = wb_id )
    current_wb.invalidate_waybill_action()
    return direct_to_template( template, {'status': 'Waybill %s has now been Removed' % current_wb.waybillNumber})


#=======================================================================================================================
# def invalidate_waybill_action( wb_id ):
#    current_wb = Waybill.objects.get( id = wb_id )
#    for lineitem in current_wb.loadingdetail_set.select_related():
#        lineitem.order_item.lti_line.restore_si( lineitem.numberUnitsLoaded )
#        lineitem.numberUnitsLoaded = 0
#        lineitem.save()
#    current_wb.invalidated = True
#    current_wb.save()
#=======================================================================================================================


@login_required
def waybill_validate_form_update( request, wb_id, queryset=Waybill.objects.all(), template='waybill/waybill_detail.html'):
    """
    Admin Edit waybill
    waybill/validate/(.*)
    waybill/waybill_detail.html
    """
    current_wb = get_object_or_404( queryset, id = wb_id )
    
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
        numberUnitsLoaded = forms.CharField( widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsGood = forms.CharField( widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsLost = forms.CharField( widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsDamaged = forms.CharField( widget = forms.TextInput( attrs = {'size':'5'} ), required = False )

        unitsLostReason = LRModelChoiceField( queryset = EpicLossDamages.objects.filter(type = 'L', comm_category_code__in = comm_cats ) , required = False )
        unitsDamagedReason = LRModelChoiceField( queryset = EpicLossDamages.objects.filter( type = 'D', comm_category_code__in = comm_cats ) , required = False )

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
    qs = Places.objects.filter( geo_name = current_lti[0].destination_loc_name, organization_id = current_lti[0].consegnee_code )
    if len( qs ) == 0:
        qs = Places.objects.filter( geo_name = current_lti[0].destination_loc_name )

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
    
    return direct_to_template( template, {
        'form': form, 'lti_list': current_lti, 
        'formset': formset, 'audit': current_audit
    })


@login_required
def waybill_view( request, wb_id, queryset=Waybill.objects.all(), template='waybill/print/waybill_detail_view.html' ):
    ## TODO: remove dependency of zippedWB
    try:
        waybill_instance = queryset.get(id = wb_id)
        zippedWB = waybill_instance.compress()
        lti_detail_items = LtiOriginal.objects.filter( code = waybill_instance.ltiNumber )
        extra_lines = 5 - waybill_instance.loadingdetail_set.select_related().count()
        my_empty = [''] * extra_lines
        
        try:
            disp_person_object = EpicPerson.objects.get( person_pk = waybill_instance.dispatcherName )
        except:
            disp_person_object = ''
            
        try:
            rec_person_object = EpicPerson.objects.get( person_pk = waybill_instance.recipientName )
        except:
            rec_person_object = ''

    except Exception as e:
        print e
        return redirect( "select_action" )
    
    return direct_to_template( template, {
        'object': waybill_instance,
        'LtiOriginal': lti_detail_items,
        'disp_person': disp_person_object,
        'rec_person': rec_person_object,
        'extra_lines': my_empty,
        'zippedWB': zippedWB,
    })


@login_required
def waybill_view_reception( request, wb_id, template='waybill/print/waybill_detail_view_reception.html' ):
    ## TODO: remove dependency of zippedWB
    
    zippedWB = ''
    try:
        waybill_instance = Waybill.objects.get( id = wb_id )
        lti_detail_items = LtiOriginal.objects.filter( code = waybill_instance.ltiNumber )
        number_of_lines = waybill_instance.loadingdetail_set.select_related().count()
        my_empty = [''] * (5 - number_of_lines)
        zippedWB = waybill_instance.compress()
    except:
        return redirect( "select_action" )
    
    rec_person_object, disp_person_object = '', ''
    try:
        disp_person_object = EpicPerson.objects.get( person_pk = waybill_instance.dispatcherName )
        rec_person_object = EpicPerson.objects.get( person_pk = waybill_instance.recipientName )
    except:
        pass
    
    return direct_to_template( template, {
        'object': waybill_instance,
        'LtiOriginal': lti_detail_items,
        'disp_person': disp_person_object,
        'rec_person': rec_person_object,
        'extra_lines': my_empty,
        'zippedWB': zippedWB,
    })


@login_required
def waybill_reception( request, wb_code, queryset=Waybill.objects.all(), template='waybill/receiveWaybill.html' ):
    # get the LTI info
    current_wb = get_object_or_404(queryset, id = wb_code )
    current_lti = current_wb.ltiNumber
    current_items = LtiWithStock.objects.filter( lti_code = current_lti )
    if  request.user.profile.isReciever or request.user.profile.superUser or request.user.profile.compasUser:
        pass
    else:
        return redirect( "waybill_view", wb_code)
    
#    current_wb.auditComment = 'Receipt Action'
#    current_wb.save()
    
    class LRModelChoiceField( forms.ModelChoiceField ):
        def label_from_instance( self, obj ):
            cause = obj.cause
            length_c = len( obj.cause ) - 10
            if length_c > 20:
                cause = obj.cause[0:20] + '...' + obj.cause[length_c:]
            return cause
    
    class LoadingDetailRecForm( forms.ModelForm ):
        order_item = forms.ModelChoiceField( queryset = current_items, label = 'Commodity' )
        for itm in ModelChoiceIterator( order_item ):
            print itm
        numberUnitsGood = forms.CharField( widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsLost = forms.CharField( widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        numberUnitsDamaged = forms.CharField( widget = forms.TextInput( attrs = {'size':'5'} ), required = False )
        comm_cats = []
        for item in  current_items :
            comm_cats.append( item.lti_line.comm_category_code )
        unitsLostReason = LRModelChoiceField( queryset = EpicLossDamages.objects.filter( type = 'L' ).filter( comm_category_code__in = comm_cats ) , required = False )
        unitsDamagedReason = LRModelChoiceField( queryset = EpicLossDamages.objects.filter( type = 'D' ).filter( comm_category_code__in = comm_cats ) , required = False )
        class Meta:
            model = LoadingDetail
            fields = ( 'wbNumber', 'order_item', 'numberUnitsGood', 'numberUnitsLost', 'numberUnitsDamaged', 'unitsLostReason',
                        'unitsDamagedReason', 'overloadedUnits', 'overOffloadUnits' )
        def clean_unitsLostReason( self ):
            #cleaned_data = self.cleaned_data
            my_losses = self.cleaned_data.get( 'numberUnitsLost' )
            my_lr = self.cleaned_data.get( 'unitsLostReason' )
            if  float( my_losses ) > 0 :
                if my_lr == None:
                    raise forms.ValidationError( _("You have forgotten to select the Loss Reason") )
            return my_lr

        def clean_unitsDamagedReason( self ):
            my_damage = self.cleaned_data.get( 'numberUnitsDamaged' )
            my_dr = self.cleaned_data.get( 'unitsDamagedReason' )
            if float( my_damage ) > 0:
                if my_dr == None:
                    raise forms.ValidationError( _("You have forgotten to select the Damage Reason") )
            return my_dr


        def clean_unitsLostType( self ):
            #cleaned_data = self.cleaned_data
            my_losses = self.cleaned_data.get( 'numberUnitsLost' )
            my_lr = self.cleaned_data.get( 'unitsLostType' )
            if  float( my_losses ) > 0 :
                if my_lr == None:
                    raise forms.ValidationError( _("You have forgotten to select the Loss Type") )
            return my_lr

        def clean_unitsDamagedType( self ):
            my_damage = self.cleaned_data.get( 'numberUnitsDamaged' )
            my_dr = self.cleaned_data.get( 'unitsDamagedType' )

            if float( my_damage ) > 0:
                if my_dr == None:
                    raise forms.ValidationError( _("You have forgotten to select the Damage Type") )
            return my_dr


        def clean( self ):
            cleaned = self.cleaned_data
            numberUnitsGood = float( cleaned.get( 'numberUnitsGood' ) )
            loadedUnits = float( self.instance.numberUnitsLoaded )
            damadgedUnits = float( cleaned.get( 'numberUnitsDamaged' ) )
            lostUnits = float( cleaned.get( 'numberUnitsLost' ) )
            totaloffload = float( numberUnitsGood + damadgedUnits + lostUnits )
            if not cleaned.get( 'overOffloadUnits' ):
                if not totaloffload == loadedUnits:
                    myerror = ''
                    if totaloffload > loadedUnits:
                        myerror = "%.3f" _("Units loaded but")" %.3f"_("units accounted for") % ( loadedUnits, totaloffload )
                    if totaloffload < loadedUnits:
                        myerror = "%.3f" _("Units loaded but only ") "%.3f" _("units accounted for") % ( loadedUnits, totaloffload )
                    self._errors['numberUnitsGood'] = self._errors.get( 'numberUnitsGood', [] )
                    self._errors['numberUnitsGood'].append( myerror )
                    raise forms.ValidationError( myerror )
            return cleaned
    LDFormSet = inlineformset_factory( Waybill, LoadingDetail, LoadingDetailRecForm, fk_name = "wbNumber", extra = 0 )

    if request.method == 'POST':

        form = WaybillRecieptForm( request.POST, instance = current_wb )

        formset = LDFormSet( request.POST, instance = current_wb )
        if form.is_valid() and formset.is_valid():
            form.recipientTitle = request.user.profile.compasUser.title
            form.recipientName = request.user.profile.compasUser.person_pk
            wb_new = form.save()
            wb_new.recipientTitle = request.user.profile.compasUser.title
            wb_new.recipientName = request.user.profile.compasUser.person_pk
            wb_new.auditComment = 'Receipt Action'
            wb_new.save()
            formset.save()
            return HttpResponseRedirect( '../viewwb_reception/' + str( current_wb.id ) ) #
        else:
            print( formset.errors )
            print( form.errors )
    else:
        if current_wb.recipientArrivalDate:
            form = WaybillRecieptForm( instance = current_wb )
            #form.instance.auditComment= 'Receipt Action'
            form.recipientTitle = request.user.profile.compasUser.title
            form.recipientName = request.user.profile.compasUser.last_name + ', ' + request.user.profile.compasUser.first_name
            #form.auditComment = 'Receipt Action'
        else:
            form = WaybillRecieptForm( instance = current_wb,
            initial = {
                'recipientArrivalDate':datetime.date.today(),
                'recipientStartDischargeDate':datetime.date.today(),
                'recipientEndDischargeDate':datetime.date.today(),
                'recipientName':       request.user.profile.compasUser.last_name + ', ' + request.user.profile.compasUser.first_name,
                'recipientTitle':       request.user.profile.compasUser.title,
                #'auditComment': 'Receipt Action',
            }
        )
        formset = LDFormSet( instance = current_wb )
    
    return direct_to_template( template, {
        'form': form, 
        'lti_list': current_lti, 
        'formset': formset
    })


@login_required
def waybill_search( request, template='waybill/list_waybills.html' ):
    search_string = ''
    isSuperUser = False
    try:
        search_string = request.GET['wbnumber']
    except:
        pass

    found_wb = Waybill.objects.filter( invalidated = False ).filter( waybillNumber__icontains = search_string )
    my_valid_wb = []

    if request.user.profile != '' :
        for waybill in found_wb:
            if request.user.profile.isCompasUser or request.user.profile.readerUser or ( request.user.profile.warehouses and waybill.origin_wh_code == request.user.profile.warehouses.origin_wh_code ) or ( request.user.profile.receptionPoints and  waybill.consegnee_code == request.user.profile.receptionPoints.consegnee_code and waybill.destination_loc_name == request.user.profile.receptionPoints.LOC_NAME ) or ( request.user.profile.isAllReceiver and waybill.consegnee_code == 'W200000475' ):
                my_valid_wb.append( waybill.id )

    if request.user.profile.superUser or request.user.profile.readerUser or request.user.profile.isCompasUser:
        isSuperUser = True

    return direct_to_template( template, {
        'waybill_list': found_wb, 
        'my_wb': my_valid_wb, 
        'isSuperUser': isSuperUser
    })


### Create Waybill 
@login_required
def waybillCreate( request, lti_code, template='waybill/createWaybill.html' ):
    # TODO: Fix COI_CODE selector possibly with hirarchical list of lti's
    c_sis = []
    current_lti = LtiOriginal.objects.filter( code = lti_code )
    current_items = LtiWithStock.objects.filter( lti_code = lti_code )
    for lti in current_lti:
        c_sis.append( lti.si_code )

    #current_stock = EpicStock.in_stock_objects.filter( si_code__in = c_sis ).filter( wh_code = current_lti[0].origin_wh_code )

    class LoadingDetailDispatchForm( forms.ModelForm ):
        order_item = forms.ModelChoiceField( queryset = current_items, label = 'Commodity' )
        #coi_code = ModelChoiceField( queryset = current_stock )
        overload = forms.BooleanField( required = False )

        class Meta:
            model = LoadingDetail
            fields = ( 'order_item', 'numberUnitsLoaded', 'wbNumber', 'overloadedUnits', 'overOffloadUnits' )# , 'coi_code' )

        def clean( self ):
            try:
                cleaned = self.cleaned_data
                order_item = cleaned.get( "order_item" )
                units = cleaned.get( "numberUnitsLoaded" )
                overloaded = cleaned.get( 'overloadedUnits' )
                max_items = order_item.lti_line.items_left
                if units > max_items + self.instance.numberUnitsLoaded and  overloaded == False: #and not overloaded:
                    myerror = "Overloaded!"
                    self._errors['numberUnitsLoaded'] = self._errors.get( 'numberUnitsLoaded', [] )
                    self._errors['numberUnitsLoaded'].append( myerror )
                    raise forms.ValidationError( myerror )
                return cleaned
            except:
                    myerror = "Value error!"
                    self._errors['numberUnitsLoaded'] = self._errors.get( 'numberUnitsLoaded', [] )
                    self._errors['numberUnitsLoaded'].append( myerror )
                    raise forms.ValidationError( myerror )

    LDFormSet = inlineformset_factory( Waybill, LoadingDetail, form = LoadingDetailDispatchForm, 
                                       fk_name = "wbNumber", formset = BaseLoadingDetailFormFormSet, 
                                       extra = 5, max_num = 5 )
    current_wh = ''
    if request.method == 'POST':
        form = WaybillForm( request.POST )
        form.fields["destinationWarehouse"].queryset = Places.objects.filter( geo_name = current_lti[0].destination_loc_name )
        formset = LDFormSet( request.POST )
        if form.is_valid() and formset.is_valid():
            wb_new = form.save()
            instances = formset.save( commit = False )
            wb_new.waybillNumber = wb_new.new_waybill_no()
            for subform in instances:
                subform.wbNumber = wb_new
                subform.save()
            wb_new.save()
            return HttpResponseRedirect( '../viewwb/' + str( wb_new.id ) )
        else:
            print( formset.errors )
            print( form.errors )
            print( formset.non_form_errors )
    else:
        qs = Places.objects.filter( geo_name = current_lti[0].destination_loc_name ).filter( organization_id = current_lti[0].consegnee_code )
        if len( qs ) == 0:
            qs = Places.objects.filter( geo_name = current_lti[0].destination_loc_name )
        else:
            current_wh = qs[0]
        form = WaybillForm( 
            initial = {
                    'dispatcherName':      request.user.profile.compasUser.person_pk,
                    'dispatcherTitle':      request.user.profile.compasUser.title,
                    'ltiNumber':         current_lti[0].code,
                    'dateOfLoading':     datetime.date.today(),
                    'dateOfDispatch':    datetime.date.today(),
                    'recipientLocation': current_lti[0].destination_loc_name,
                    'recipientConsingee':current_lti[0].consegnee_name,
                    'transportContractor': current_lti[0].transport_name,
                    'invalidated':'False',
                    'destinationWarehouse':current_wh,
                    'waybillNumber':'N/A'
                }
        )
        form.fields["destinationWarehouse"].queryset = qs

        formset = LDFormSet()
    return direct_to_template( template, {
        'form': form, 
        'lti_list':current_lti, 
        'formset':formset
    })


@login_required
def waybill_edit( request, wb_id, template='waybill/createWaybill.html' ):
    try:
        current_wb = Waybill.objects.get( id = wb_id )
        lti_code = current_wb.ltiNumber
        current_lti = LtiOriginal.objects.filter( code = lti_code )
        current_items = LtiWithStock.objects.filter( lti_code = lti_code )
    except Exception as e:
        print e
        current_wb = ''
    
    class LoadingDetailDispatchForm( forms.ModelForm ):
        order_item = forms.ModelChoiceField( queryset = current_items, label = 'Commodity' )
        class Meta:
            model = LoadingDetail
            fields = ( 'id', 'order_item', 'numberUnitsLoaded', 'wbNumber', 'overloadedUnits' )
        def clean( self ):
            try:
                cleaned = self.cleaned_data

                #order_item = cleaned.get( 'order_item' )
                units = cleaned.get( "numberUnitsLoaded" )
                overloaded = cleaned.get( 'overloadedUnits' )
                max_items = self.instance.numberUnitsLoaded

                if units > max_items + self.instance.numberUnitsLoaded and overloaded == False:
                        myerror = "Overloaded!"
                        self._errors['numberUnitsLoaded'] = self._errors.get( 'numberUnitsLoaded', [] )
                        self._errors['numberUnitsLoaded'].append( myerror )
                        raise forms.ValidationError( myerror )
                return cleaned
            except Exception as e:
                    myerror = "Value error!"
                    self._errors['numberUnitsLoaded'] = self._errors.get( 'numberUnitsLoaded', [] )
                    self._errors['numberUnitsLoaded'].append( myerror )
                    raise forms.ValidationError( myerror )
    LDFormSet = inlineformset_factory( Waybill, LoadingDetail, LoadingDetailDispatchForm, fk_name = "wbNumber", formset = BaseLoadingDetailFormFormSet, extra = 5, max_num = 5 )
    if request.method == 'POST':
        form = WaybillForm( request.POST, instance = current_wb )
        formset = LDFormSet( request.POST, instance = current_wb )
        if form.is_valid() and formset.is_valid():
            wb_new = form.save()
            formset.save()
            return redirect("waybill_view", wb_new.id )
    else:
        form = WaybillForm( instance = current_wb )
        form.fields["destinationWarehouse"].queryset = Places.objects.filter( geo_name = current_lti[0].destination_loc_name )
        formset = LDFormSet( instance = current_wb )
    
    return direct_to_template( template, {
        'form': form, 
        'lti_list':current_lti, 
        'formset':formset
    })


@login_required
def waybill_validate_dispatch_form( request, template='validate/validateForm.html' ):
    ValidateFormset = modelformset_factory( Waybill, fields = ( 'id', 'waybillValidated', ), extra = 0 )
    validatedWB = Waybill.objects.filter( invalidated = False ).filter( waybillValidated = True ).filter( waybillSentToCompas = False )
    issue = ''
    errorMessage = _('Problems with Stock, Not enough in Dispatch Warehouse')
    if request.method == 'POST':
        formset = ValidateFormset( request.POST, WaybillValidationFormset )
        if  formset.is_valid() :
            instances = formset.save( commit = False )
            for waybill in instances:
                try:
                    if waybill.check_lines():
                        waybill.auditComment = _('Validated Dispatch')
                        try:
                            errorlog = CompasLogger.objects.get( wb = waybill )
                            errorlog.user = ''
                            errorlog.errorDisp = ''
                            errorlog.timestamp = datetime.datetime.now()
                            errorlog.save()
                        except:
                            pass
                    else:
                        waybill.auditComment = _('Tried to Validate Dispatch')
                        issue = _('Problems with Stock on WB:  ' )+ str( waybill )
                        waybill.waybillValidated = False
                        messages.add_message( request, messages.ERROR, issue )
                        create_or_update(waybill, request.user, errorMessage)
                except:
                        waybill.auditComment = _('Tried to Validate Dispatch')
                        issue = _('Problems with Stock on WB:  ') + str( waybill )
                        waybill.waybillValidated = False
                        messages.add_message( request, messages.ERROR, issue )
                        create_or_update(waybill, request.user, errorMessage)

            formset.save()
    waybills = Waybill.objects.filter( invalidated = False, waybillValidated = False, dispatcherSigned = True )
    formset = ValidateFormset( queryset = waybills )
    
    return direct_to_template( template, {
        'formset': formset, 
        'validatedWB': validatedWB
    })

@login_required
def waybill_validate_receipt_form( request, template='validate/validateReceiptForm.html' ):
    ValidateFormset = modelformset_factory( Waybill, fields = ( 'id', 'waybillReceiptValidated', ), extra = 0 )
    validatedWB = Waybill.objects.filter( invalidated = False ).filter( waybillReceiptValidated = True ).filter( waybillRecSentToCompas = False ).filter( waybillSentToCompas = True )
    errorMessage = _('Problems with Waybill, More Offloaded than Loaded, Update Dispatched Units!')
    if request.method == 'POST':
        formset = ValidateFormset( request.POST )
        if  formset.is_valid():
            instances = formset.save( commit = False )
            for waybill in  instances:
                if waybill.check_lines_receipt():
                    waybill.auditComment = _('Validated Receipt')
                    
                    CompasLogger.objects.filter( wb = waybill )\
                                .update(user = request.user, errorRec = '', timestamp = datetime.datetime.now())
                    
                else:
                    waybill.auditComment = _('Tried to Validate Receipt')
                    messages.add_message( request, messages.ERROR, _('Problems with Stock on WB:')' %s' % waybill )
                    waybill.waybillReceiptValidated = False
                    create_or_update(waybill, request.user, errorMessage)
                    
            formset.save()

    waybills = Waybill.objects.filter( invalidated = False ).filter( waybillReceiptValidated = False ).filter( recipientSigned = True ).filter( waybillValidated = True )
    formset = ValidateFormset( queryset = waybills )

    return direct_to_template( template, {
        'formset': formset, 
        'validatedWB': validatedWB
    })


# Shows a page with the Serialized Waybill in comressed & uncompressed format
@login_required
def serialize( request, wb_code, template='blank.html', queryset=Waybill.objects.all() ):
    waybill = get_object_or_404(queryset, id = wb_code )
    
    return direct_to_template( template, {
        'status': waybill.serialize(), 
        'ziped': waybill.compress(), 
        'wb_code': wb_code,
    })

## receives a POST with the compressed or uncompressed WB and sends you to the Receive WB 
@login_required
def deserialize( request ):
    waybillnumber = ''
    wb_data = request.POST['wbdata']
    wb_serialized = ''
    if wb_data[0] == '[':
        wb_serialized = wb_data
    else:
        wb_serialized = un64unZip( wb_data )
    
    for obj in serializers.deserialize( "json", wb_serialized ):
        if type( obj.object ) is Waybill:
            waybillnumber = obj.object.id
    
    return redirect(waybill_reception, waybillnumber )

#=======================================================================================================================
# ## Serialization of fixtures    
# def fixtures_serialize():
#    # serialise each of the fixtures 
#    #     DispatchPoint
#    dispatchPointsData = DispatchPoint.objects.all()
#    receptionPointData = ReceptionPoint.objects.all()
#    packagingDescriptonShort = PackagingDescriptionShort.objects.all()
#    #lossesDamagesReason = LossesDamagesReason.objects.all()
#    #lossesDamagesType = LossesDamagesType.objects.all()
#    serialized_data = serializers.serialize( 'json', list( dispatchPointsData ) + list( receptionPointData ) + list( packagingDescriptonShort ) )
#    init_file = open( 'waybill/fixtures/initial_data.json', 'w' )
#    init_file.writelines( serialized_data )
#    init_file.close()
#=======================================================================================================================

#=======================================================================================================================
# def custom_show_toolbar( request ):
#    return True
#=======================================================================================================================

#=======================================================================================================================
# def view_stock( request, template='stock/stocklist.html' ):
#    stocklist = EpicStock.objects.all()
#    return render_to_response(template, {'stocklist':stocklist})
#=======================================================================================================================

def viewLogView( request, template='status.html' ):
    return direct_to_template( template, {'status': '<h3>Log view</h3><pre>%s</pre>' % viewLog()})

def profile( request, template='status.html' ):
    return direct_to_template(template, {'status': request.user.get_profile()})


def expand_response(response, **headers):
    for header, value in headers.items():
        response[header] = value
    return response

#Reports 
def ltis_report( request, template='reporting/list_ltis.txt' ):
    ltis = LtiOriginal.objects.all()
    items = LtiWithStock.objects.filter( lti_line__in = ltis )
    listIt = []
    for line in items:
        if line.loadingdetail_set.select_related():
            for x in line.loadingdetail_set.select_related():
                myList = []
                myList = [x, line.lti_line]
                listIt.append( myList )
        else:
            myList = ['', line.lti_line]
            listIt.append( myList )

    return expand_response(direct_to_template(template, {'ltis': listIt}, mimetype = 'text/csv'),
                           **{'Content-Disposition': 'attachment; filename=list-%s.csv' % datetime.date.today()})

def dispatch_report_wh( request, wh, template='reporting/list_ltis.txt' ):
    ltis = LtiOriginal.objects.filter( origin_wh_code = wh )
    items = LtiWithStock.objects.filter( lti_line__in = ltis )
    listIt = []
    for line in items:
        if line.loadingdetail_set.select_related():
            for x in line.loadingdetail_set.select_related():
                myList = []
                myList = [x, line.lti_line]
                listIt.append( myList )
        else:
            myList = ['', line.lti_line]
            listIt.append( myList )

    return expand_response(direct_to_template(template, {'ltis': listIt}, mimetype = 'text/csv'),
                           **{'Content-Disposition': 'attachment; filename=list-%s-%s.csv' % (wh, datetime.date.today())})


def receipt_report_wh( request, loc, cons, template='reporting/list_ltis.txt' ):
    ltis = LtiOriginal.objects.filter( destination_location_code = loc ).filter( consegnee_code = cons )
    items = LtiWithStock.objects.filter( lti_line__in = ltis )
    listIt = []
    for line in items:
        if line.loadingdetail_set.select_related():
            for x in line.loadingdetail_set.select_related():
                myList = []
                myList = [x, line.lti_line]
                listIt.append( myList )
        else:
            myList = ['', line.lti_line]
            listIt.append( myList )
    
    return expand_response(direct_to_template(template, {'ltis': listIt}, mimetype = 'text/csv'),
                           **{'Content-Disposition': 'attachment; filename=receipt-%s-%s.csv' % (loc, datetime.date.today())})
    

def receipt_report_cons( request, cons, template='reporting/list_ltis.txt' ):
    ltis = LtiOriginal.objects.filter( consegnee_code = cons )
    items = LtiWithStock.objects.filter( lti_line__in = ltis )
    listIt = []
    for line in items:
        if line.loadingdetail_set.select_related():
            for x in line.loadingdetail_set.select_related():
                myList = []
                myList = [x, line.lti_line]
                listIt.append( myList )
        else:
            myList = ['', line.lti_line]
            listIt.append( myList )

    return expand_response(direct_to_template(template, {'ltis': listIt}, mimetype = 'text/csv'))


#=======================================================================================================================
#    response = HttpResponse( mimetype = 'text/csv' )
# #    response['Content-Disposition'] = 'attachment; filename=list-' + str( datetime.date.today() ) + '.csv'
#    t = loader.get_template( 'reporting/list_ltis.txt' )
#    c = Context( {
#            'ltis': listIt,
#        } )
#    response.write( t.render( c ) )
#    return response
#=======================================================================================================================

#=======================================================================================================================
# def select_report( request ):
#    return render_to_response( 'reporting/select_report.html', context_instance = RequestContext( request ) )
#=======================================================================================================================

def select_data( request, template='reporting/select_data.html', form_class=WarehouseForm ):
    form = form_class( request.POST or None )
    context = not form.is_valid() and {'form': form, } or {}
    return direct_to_template(request, template, context)

def barcode_qr( request, wb ):
#    import sys
#    if sys.platform == 'darwin':
#        from qrencode import Encoder
#        enc = Encoder()
#        myz = wb_compress( wb )
#        im = enc.encode( myz, { 'width': 350 } )
#        response = HttpResponse( mimetype = "image/png" )
#        im.save( response, "PNG" )
#    else:
    import subprocess
    myz = wb.compress()
    mydata = subprocess.Popen( ['zint', '--directpng', '--barcode=58', '-d%s' % myz ], stdout = subprocess.PIPE )
    image = mydata.communicate()[0]
    #print mydata.communicate()
    return HttpResponse( image, mimetype = "Image/png" )

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


@csrf_exempt
def get_synchronize_stock( request ):
    '''
    This method is called by the offline application.
    The stocks identified by the warehouse_code in request are serialized and sended to the offline application.
    '''

    warehouse_code = request.GET['warehouse_code']
    stocks_list = EpicStock.objects.filter( wh_code = warehouse_code )

    #from kiowa.db.utils import instance_as_dict

    return HttpResponse(simplejson.dumps( [model_to_dict( element ) for element in stocks_list], use_decimal=True), 
                        content_type="application/json; charset=utf-8")


@csrf_exempt
def get_synchronize_lti( request ):
    '''
    This method is called by the offline application.
    The ltis identified by the warehouse_code in request are serialized and sended to the offline application.
    '''

    warehouse_code = request.GET['warehouse_code']

#        from waybill.models import LtiOriginal    
    ltis_list = LtiOriginal.objects.filter( origin_wh_code = warehouse_code )

    #from kiowa.db.utils import instance_as_dict

    return HttpResponse(simplejson.dumps( [model_to_dict( element ) for element in ltis_list], use_decimal=True), 
                        content_type="application/json; charset=utf-8")
    

def get_wb_stock( request, queryset=DispatchPoint.objects.all() ):
    warehouse = get_object_or_404(queryset, pk = request.GET['warehouse'])
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
    


@csrf_exempt
def get_synchronize_waybill( request ):
    '''
    This method is called by the offline application.
    The waybills that has the destinationWarehause equal to warehouse_code in request are serialized and sended to the offline application.
    '''

    warehouse_code = request.GET['warehouse_code']

    #from waybill.models import Waybill    
    waybills_list = Waybill.objects.filter( destinationWarehouse__pk = warehouse_code )
    #from kiowa.db.utils import instance_as_dict
    
    return HttpResponse(simplejson.dumps( [model_to_dict( element ) for element in waybills_list], use_decimal=True), 
                        content_type="application/json; charset=utf-8")
    

def get_synchronize_waybill2( request ):
    '''
    This method is called by the offline application.
    The waybills that has the destinationWarehause equal to warehouse_code in request are serialized and sended to the offline application.
    '''
    try:
        warehouse_code = request.GET['warehouse_code']
    except:
        warehouse_code = 'CCBJ004'
    ld = []
    ltis = []
    stck = []
    #from waybill.models import Waybill    
    waybills_list = Waybill.objects.filter( destinationWarehouse = warehouse_code )
    for waybill_to_serialize in waybills_list:
        loadingdetails_to_serialize = waybill_to_serialize.loadingdetail_set.select_related()
        # Add related LtiOriginals to serialized representation
        ltis_to_serialize = LtiOriginal.objects.filter( code = waybill_to_serialize.ltiNumber )
        # Add related EpicStocks to serialized representation
        stocks_to_serialize = []
        for lti in ltis_to_serialize:
            for s in lti.stock_items():
                stocks_to_serialize.append( s )
        ld += loadingdetails_to_serialize
        ltis += ltis_to_serialize
        stck += stocks_to_serialize

    data = serializers.serialize( 'json', list( waybills_list ) + list( ld ) + list( ltis ) + list( stck ) )

    ## testing it to see deser
    print data
    for deserialized_object in serializers.deserialize( "json", data ):

        print deserialized_object

    response = HttpResponse( data, mimetype = 'application/json' )

    return response

@csrf_exempt
def get_all_data( request ):
    print 'See'
    return HttpResponse(serialized_all_items(), 
                        content_type="application/json; charset=utf-8")

@csrf_exempt
def get_all_data_download( request ):
    print 'Donwload'
    return expand_response(HttpResponse(serialized_all_items(), content_type='text/csv'),
                           **{'Content-Disposition': 'attachment; filename=data-%s-%s.csv' % 
                              (settings.COMPAS_STATION, datetime.date.today())})
    
    #===================================================================================================================
    # data = serialized_all_items()
    # response = HttpResponse( mimetype = 'text/csv' )
    # response['Content-Disposition'] = 'attachment; filename=data-' + settings.COMPAS_STATION + '-' + str( datetime.date.today() ) + '.csv'
    # response.write( data )
    # return response
    #===================================================================================================================

#=======================================================================================================================
# def testing():
#    print 'c'
#    mylti = LtiOriginal.objects.filter( code = 'ISBX002110025392P' )
#=======================================================================================================================
