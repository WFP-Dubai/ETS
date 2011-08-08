import datetime

from django.forms import ModelForm
from django.forms.models import  BaseModelFormSet, BaseInlineFormSet
from django import forms
#from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from ets import models as ets_models

UNDEFINED_MESSAGE = "N/A"

class WarehouseChoiceForm( forms.Form ):
    warehouse = forms.ModelChoiceField( queryset = ets_models.Warehouse.objects.filter( start_date__lt = datetime.date.today() ) )

class WaybillForm( ModelForm ):
    
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

class WaybillRecieptForm( ModelForm ):
    
    def __init__(self, **kwargs):
        super(WaybillRecieptForm, self).__init__(**kwargs)
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

class BaseLoadingDetailFormFormSet( BaseInlineFormSet ):
    
    def append_non_form_error( self, message ):
        errors = super( BaseLoadingDetailFormFormSet, self ).non_form_errors()
        errors.append( message )
        raise forms.ValidationError( errors )
    
    def clean( self ):
        count = 0
        for form in self.forms:
            if form.is_bound:
                #TODO: remove try..except or specify error types
                try:
                    if form.cleaned_data.get( 'numberUnitsLoaded' ):
                        count += 1
                except:
                    pass
        
        if count < 1:
            raise forms.ValidationError( _('You must have at least one commodity') )


class WaybillFullForm( ModelForm ):

    def __init__(self, **kwargs):
        super(WaybillFullForm,self).__init__(**kwargs)
        self.fields['auditComment'].required = True
    
    class Meta:
        model = ets_models.Waybill
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
            'transportDeliverySigned': forms.HiddenInput,
            'transportDeliverySignedTimestamp': forms.HiddenInput,
            'transportDispachSigned': forms.HiddenInput,
            'transportDispachSignedTimestamp': forms.HiddenInput,
            'recipientName': forms.HiddenInput,
            'recipientTitle': forms.HiddenInput,
            'recipientLocation': forms.HiddenInput,
            'recipientConsingee': forms.HiddenInput,
            'recipientRemarks': forms.TextInput( attrs = {'size':'40'} ),
            'recipientSignedTimestamp': forms.HiddenInput,
            'waybillNumber': forms.HiddenInput,
            'invalidated': forms.HiddenInput,
            'auditComment': forms.Textarea,
        }
    
    def thisDispName( self ):
        try:
            name = ets_models.EpicPerson.objects.get( person_pk = self.instance.dispatcherName )
        except ets_models.EpicPerson.DoesNotExist:
            name = UNDEFINED_MESSAGE
        return name
    
    def thisRecName( self ):
        try:
            name = ets_models.EpicPerson.objects.get( person_pk = self.instance.recipientName )
        except ets_models.EpicPerson.DoesNotExist:
            name = UNDEFINED_MESSAGE
        return name

class WaybillValidationFormset( BaseModelFormSet ):
    def clean( self ):
        issue = ''
        super( WaybillValidationFormset, self ).clean()
        for form in self.forms:
            if not form.check_lines():
                #TODO: Refactor it
                valid = False
                issue += ' WB: ' + str( form )
                raise form.ValidationError( _("You have an error") )
            
            if not valid:
                ##TODO: cleanup such things
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
        fields = ( 
            'order_item', 'numberUnitsLoaded', 'numberUnitsGood', 
            'numberUnitsLost', 'numberUnitsDamaged', 'unitsLostReason', 
            'unitsDamagedReason', 
        )
