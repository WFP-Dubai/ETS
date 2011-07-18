import datetime

from django.forms import ModelForm
from django.forms.models import  BaseModelFormSet, BaseInlineFormSet
from django import forms
#from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from ets import models as ets_models

class WarehouseForm( forms.Form ):
    warehouse = forms.ModelChoiceField( queryset = ets_models.DispatchPoint.objects.filter( ACTIVE_START_DATE__lt = datetime.date.today() ) )

class WaybillForm( ModelForm ):
    
    #===================================================================================================================
    # dateOfLoading = forms.DateField(_("Date of loading"))
    # dateOfDispatch = forms.DateField(_("Date of Dispatch"))
    # transportType = forms.CharField(_("Transport Type"), widget = forms.Select( choices = Waybill.transport_type ) )
    # transactionType = forms.CharField(_("Transaction Type"), widget = forms.Select( choices = Waybill.transaction_type_choice ) )
    #===================================================================================================================

    #===================================================================================================================
    # dispatchRemarks = forms.CharField(_("Dispatch Remarks"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # ltiNumber = forms.CharField(_("LTI Number"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # transportContractor = forms.CharField(_("Transport Contractor"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # transportSubContractor = forms.CharField(_("Transport SubContractor"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # transportDriverName = forms.CharField(_("Transport DriverName"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # transportDriverLicenceID = forms.CharField(_("Transport DriverLicenceID"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # transportVehicleRegistration = forms.CharField(_("Transport Vehicle Registration"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # dispatcherName = forms.CharField(_("Dispatcher Name"), widget = forms.HiddenInput(), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # dispatcherTitle = forms.CharField(_("Dispatcher Title"), widget = forms.HiddenInput(), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # transportTrailerRegistration = forms.CharField(_("Transport Trailer Registration "), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # recipientLocation = forms.CharField(_("Recipient Location"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # recipientConsingee = forms.CharField(_("Recipient Consingee"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # waybillNumber = forms.CharField(_("Waybill Number"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # destinationWarehouse = ModelChoiceField(_("Destination Warehouse "), queryset = Places.objects.all() )
    #===================================================================================================================
    #===================================================================================================================
    # invalidated = forms.CharField(_("Invalidated"), widget = forms.HiddenInput(), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # auditComment = forms.CharField(_("Audit Comment"), widget = forms.HiddenInput(), required = False )
    #===================================================================================================================

    class Meta:
        model = ets_models.Waybill
        fields = (
            'ltiNumber',
            'waybillNumber',
            'dateOfLoading',
            'dateOfDispatch',
            'transactionType',
            'transportType',
            'dispatchRemarks',
            'dispatcherName',
            'dispatcherTitle',
            'destinationWarehouse',
            'transportContractor',
            'transportSubContractor',
            'transportDriverName',
            'transportDriverLicenceID',
            'transportVehicleRegistration',
            'transportTrailerRegistration',
            'transportDispachSigned',
            'containerOneNumber',
            'containerTwoNumber',
            'containerOneSealNumber',
            'containerTwoSealNumber',
            'containerOneRemarksDispatch',
            'containerTwoRemarksDispatch',
            'recipientLocation',
            'recipientConsingee',
            'auditComment',
        )
        widgets = {
            'dispatchRemarks': forms.TextInput( attrs = {'size':'40'} ),
            'ltiNumber': forms.HiddenInput,
            'transportContractor': forms.HiddenInput,
            'transportSubContractor': forms.TextInput( attrs = {'size':'40'} ),
            'transportDriverName': forms.TextInput( attrs = {'size':'40'} ),
            'transportDriverLicenceID': forms.TextInput( attrs = {'size':'40'} ),
            'transportVehicleRegistration': forms.TextInput( attrs = {'size':'40'} ),
            'dispatcherName': forms.HiddenInput,
            'dispatcherTitle': forms.HiddenInput,
            'transportTrailerRegistration': forms.TextInput( attrs = {'size':'40'} ),
            'recipientLocation': forms.HiddenInput,
            'recipientConsingee': forms.HiddenInput,
            'waybillNumber': forms.HiddenInput,
            'invalidated': forms.HiddenInput,
            'auditComment': forms.HiddenInput,
        }
    
#=======================================================================================================================
#    def clean( self ):
#        cleaned = super(WaybillForm, self).clean()
#        dateOfDispatch = cleaned.get( 'dateOfDispatch' )
#        dateOfLoading = cleaned.get( 'dateOfLoading' )
#        
#        if dateOfDispatch and dateOfLoading:
#            if dateOfLoading > dateOfDispatch:
#                message = _("Cargo Dispatched before being Loaded")
#                #=======================================================================================================
#                # self._errors['dateOfDispatch'] = self._errors.get( 'dateOfDispatch', [] )
#                # self._errors['dateOfDispatch'].append( myerror )
#                #=======================================================================================================
#                raise forms.ValidationError( message )
# 
#        return cleaned
#=======================================================================================================================

class WaybillRecieptForm( ModelForm ):
    #===================================================================================================================
    # recipientArrivalDate = forms.DateField(_("Recipient Arrival Date"))
    #===================================================================================================================
    #===================================================================================================================
    # recipientStartDischargeDate = forms.DateField(_("Recipient Start Discharge Date"))
    #===================================================================================================================
    #===================================================================================================================
    # recipientEndDischargeDate = forms.DateField(_("Recipient End Discharge Date"))
    #===================================================================================================================
    #===================================================================================================================
    # waybillNumber = forms.CharField(_("Waybill Number"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # recipientLocation = forms.CharField(_("Recipient Location"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # recipientRemarks = forms.CharField(_("Recipient Remarks"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # recipientConsingee = forms.CharField(_("Recipient Consingee"), widget = forms.HiddenInput() )
    #===================================================================================================================
    #===================================================================================================================
    # invalidated = forms.CharField(_("Invalidated "), widget = forms.HiddenInput(), required = False )
    #===================================================================================================================
    #===================================================================================================================
    # auditComment = forms.CharField(_("Audit Comment"), widget = forms.HiddenInput(), required = False )
    #===================================================================================================================
    
    def __init__(self, **kwargs):
        self.fields['recipientArrivalDate'].required = True
        self.fields['recipientStartDischargeDate'].required = True
        self.fields['recipientEndDischargeDate'].required = True
        
    class Meta:
        model = ets_models.Waybill
        fields = (
            'waybillNumber',
            'recipientLocation',
            'recipientConsingee',
            'recipientArrivalDate',
            'recipientStartDischargeDate',
            'recipientEndDischargeDate',
            'recipientDistance',
            'recipientRemarks',
            'recipientSigned',
            'recipientSignedTimestamp',
            'transportDeliverySigned',
            'containerOneRemarksReciept',
            'containerTwoRemarksReciept',
            'invalidated',
            'auditComment',
        )
        widgets = {
            'waybillNumber': forms.HiddenInput,
            'recipientLocation': forms.HiddenInput,
            'recipientRemarks': forms.TextInput( attrs = {'size':'40'} ),
            'recipientConsingee': forms.HiddenInput,
            'invalidated': forms.HiddenInput,
            'auditComment': forms.HiddenInput,
        }

#=======================================================================================================================
#    def clean( self ):
#        cleaned = self.cleaned_data
#        print self.instance.dateOfDispatch
#        dispatch_date = self.instance.dateOfDispatch
#        arrival_date = cleaned.get( 'recipientArrivalDate' )
#        discharge_start = cleaned.get( 'recipientStartDischargeDate' )
#        discharge_end = cleaned.get( 'recipientEndDischargeDate' )
#        faults = False
#        if arrival_date < dispatch_date:
#            myerror = ''
#            myerror = _("Cargo arrived before being dispatched")
#            self._errors['recipientArrivalDate'] = self._errors.get( 'recipientArrivalDate', [] )
#            self._errors['recipientArrivalDate'].append( myerror )
#            faults = True
# 
#        if discharge_start < arrival_date:
#            myerror = ''
#            myerror = _("Cargo Discharge started before Arrival?")
#            self._errors['recipientStartDischargeDate'] = self._errors.get( 'recipientStartDischargeDate', [] )
#            self._errors['recipientStartDischargeDate'].append( myerror )
#            faults = True
# 
#        if discharge_end < discharge_start:
#            myerror = ''
#            myerror = _("Cargo finished Discharge before Starting?")
#            self._errors['recipientEndDischargeDate'] = self._errors.get( 'recipientEndDischargeDate', [] )
#            self._errors['recipientEndDischargeDate'].append( myerror )
#            faults = True
# 
#        if faults:
#            raise forms.ValidationError( myerror )
# 
#        return cleaned
#=======================================================================================================================

class BaseLoadingDetailFormFormSet( BaseInlineFormSet ):
    def append_non_form_error( self, message ):
        errors = super( BaseLoadingDetailFormFormSet, self ).non_form_errors()
        errors.append( message )
        raise forms.ValidationError( errors )
    def clean( self ):
        count = 0
        for form in self.forms:
            if form.is_bound:
                try:
                    if form.cleaned_data.get( 'numberUnitsLoaded' ):
                        count += 1
                except:
                    pass
        if count < 1:
            raise forms.ValidationError( _('You must have at least one commodity') )


class WaybillFullForm( ModelForm ):


    dateOfDispatch = forms.DateField(_("date Of Dispatch"), required = False )
    dateOfLoading = forms.DateField(_("date Of Loading"), required = False )
    dispatchRemarks = forms.CharField(_("dispatch Remarks"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    dispatcherName = forms.CharField(_("dispatcher Name"), widget = forms.HiddenInput(), required = False )
    dispatcherTitle = forms.CharField(_("dispatcher Title"), widget = forms.HiddenInput(), required = False )
    invalidated = forms.CharField(_("Invalidated"), widget = forms.HiddenInput(), required = False )
    ltiNumber = forms.CharField(_("LTI Number"), widget = forms.HiddenInput(), required = False )
    recipientArrivalDate = forms.DateField(_("Recipient Arrival Date"), required = False )
    recipientConsingee = forms.CharField(_("Recipient Consingee"), widget = forms.HiddenInput(), required = False )
    recipientConsingee = forms.CharField(_("Recipient Consingee"), widget = forms.HiddenInput(), required = False )
    recipientEndDischargeDate = forms.DateField(_("Recipient End DischargeDate"), required = False )
    recipientLocation = forms.CharField(_("Recipient Location"), widget = forms.HiddenInput(), required = False )
    recipientName = forms.CharField(_("Recipient Name"), widget = forms.HiddenInput(), required = False )
    recipientRemarks = forms.CharField(_("Recipient Remarks"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    recipientSignedTimestamp = forms.DateTimeField(_("Recipient Signed Timestamp"), widget = forms.HiddenInput(), required = False )
    recipientStartDischargeDate = forms.DateField(_("Recipient Start DischargeDate"), required = False )
    recipientTitle = forms.CharField(_("Recipient Title"), widget = forms.HiddenInput(), required = False )
    transactionType = forms.CharField(_("Transaction Type"), widget = forms.Select( choices = Waybill.TRANSACTION_TYPES ) )
    transportContractor = forms.CharField(_("Transport Contractor"), widget = forms.HiddenInput(), required = False )
    transportDeliverySigned = forms.CharField(_("Transport Delivery Signed"), widget = forms.HiddenInput(), required = False )
    transportDeliverySignedTimestamp = forms.DateTimeField(_("Transport Delivery SignedTimestamp"), widget = forms.HiddenInput(), required = False )
    transportDispachSigned = forms.CharField(_("Transport DispachSigned"), widget = forms.HiddenInput(), required = False )
    transportDispachSignedTimestamp = forms.DateTimeField( _(""),widget = forms.HiddenInput(), required = False )
    transportDriverLicenceID = forms.CharField(_("Transport Driver LicenceID"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    transportDriverName = forms.CharField(_("Transport DriverName"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    transportSubContractor = forms.CharField(_("Transport SubContractor"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    transportTrailerRegistration = forms.CharField(_("Transport Trailer Registration"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    transportType = forms.CharField(_("Transport Type"), widget = forms.Select( choices = Waybill.TRANSPORT_TYPES ) )
    transportVehicleRegistration = forms.CharField(_("Transport Vehicle Registration"), widget = forms.TextInput( attrs = {'size':'40'} ), required = False )
    waybillNumber = forms.CharField(_("Waybill Number"), widget = forms.HiddenInput(), required = False )
    auditComment = forms.CharField(_("Audit Comment"), widget = forms.Textarea, required = True )
    class Meta:
        model = ets_models.Waybill

    def thisDispName( self ):
        try:
            name = ets_models.EpicPerson.objects.get( person_pk = self.instance.dispatcherName )
        except:
            name = 'N/A'
        return name
    def thisRecName( self ):
        try:
            name = ets_models.EpicPerson.objects.get( person_pk = self.instance.recipientName )
        except:
            name = 'N/A'
        return name

class WaybillValidationFormset( BaseModelFormSet ):
    def clean( self ):
        issue = ''
        super( WaybillValidationFormset, self ).clean()
        for form in self.forms:
            if form.check_lines():
                pass
            else:
                valid = False
                issue += ' WB: ' + str( form )
                raise form.ValidationError( _("You have an error") )
            if valid:
                pass
            else:
                print issue


class MyModelChoiceField( forms.ModelChoiceField ):
    def label_from_instance( self, obj ):
        return "%s - %s" % ( obj.si_code , obj.cmmname )

class LoadingDetailDispatchForm( ModelForm ):
    class Meta:
        model = ets_models.LoadingDetail
        fields = ( 'order_item', 'numberUnitsLoaded' )


class LoadingDetailRecieptForm( ModelForm ):
    class Meta:
        model = ets_models.LoadingDetail
        fields = ( 'order_item', 'numberUnitsLoaded', 'numberUnitsGood', 'numberUnitsLost', 'numberUnitsDamaged', 'unitsLostReason', 'unitsDamagedReason', )
