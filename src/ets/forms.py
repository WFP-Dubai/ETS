import datetime

from django.forms import ModelForm
from django.forms.models import  BaseModelFormSet, BaseInlineFormSet
from django import forms
#from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from uni_form.helpers import FormHelper, Layout, Fieldset, Row

from ets import models as ets_models

UNDEFINED_MESSAGE = "N/A"

class WarehouseChoiceForm( forms.Form ):
    warehouse = forms.ModelChoiceField( queryset = ets_models.Warehouse.objects.filter( start_date__lt = datetime.date.today() ) )

class WaybillSearchForm( forms.Form ):
    q = forms.CharField(required=False, label=_('Waybill code'))


class DispatchWaybillForm( ModelForm ):
    
    def __init__(self, **kwargs):
        super(DispatchWaybillForm, self).__init__(**kwargs)
        self.fields['loading_date'].required = True
        self.fields['dispatch_date'].required = True
        
    class Meta:
        model = ets_models.Waybill
        fields = (
            'loading_date',
            'dispatch_date',
            'destination',
            'transaction_type',
            'transport_type',
            'dispatch_remarks',
            
            'transport_sub_contractor',
            'transport_driver_name',
            'transport_driver_licence',
            'transport_vehicle_registration',
            'transport_trailer_registration',
            
            'container_one_number',
            'container_two_number',
            'container_one_seal_number',
            'container_two_seal_number',
            'container_one_remarks_dispatch',
            'container_two_remarks_dispatch',
        )
        widgets = {
            'dispatch_remarks': forms.TextInput( attrs = {'size':'40'} ),
        }
    
    helper = FormHelper()
    
    # create the layout object
    helper.add_layout(Layout(
        Fieldset('Date', Row('loading_date', 'dispatch_date')),
        Fieldset('General',
                'destination',
                Row('transaction_type', 'transport_type'),
                'dispatch_remarks',
                 ),
        Fieldset('Transport',
                 'transport_sub_contractor',
                 Row('transport_driver_name', 'transport_driver_licence'),
                 Row('transport_vehicle_registration', 'transport_trailer_registration'),
                 ),
        Fieldset('Container',
                 Row('container_one_number', 'container_one_seal_number', 'container_one_remarks_dispatch'),
                 Row('container_two_number', 'container_two_seal_number', 'container_two_remarks_dispatch'),
                 )
    ))
                      
    #helper.add_input(Submit('add', _('Create waybill')))
    helper.form_tag = False


class LoadingDetailDispatchForm( forms.ModelForm ):
    stock_item = forms.ModelChoiceField(queryset=ets_models.StockItem.objects.all(), label=_('Commodity'))
    overload = forms.BooleanField( required = False )

    class Meta:
        model = ets_models.LoadingDetail
        fields = ( 'number_of_units', 'overloaded_units', 'over_offload_units' )


class BaseLoadingDetailFormFormSet( BaseInlineFormSet ):
    
    def append_non_form_error( self, message ):
        errors = super( BaseLoadingDetailFormFormSet, self ).non_form_errors()
        errors.append( message )
        raise forms.ValidationError( errors )
    
    def clean( self ):
        super(BaseLoadingDetailFormFormSet, self).clean()
        count = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if form.is_bound and getattr(form, 'cleaned_data', {}).get('number_of_units'):
                count += 1
        
        if count < 1:
            raise forms.ValidationError( _('You must have at least one commodity') )
    
    helper = FormHelper()
    
    # create the layout object
    helper.add_layout(Layout(Row('stock_item', 'number_of_units', 'overloaded_units', 
                                 'over_offload_units', 'overload', 'DELETE' )))
    helper.formset_tag = False


class WaybillRecieptForm( ModelForm ):
    
    def __init__(self, **kwargs):
        super(WaybillRecieptForm, self).__init__(**kwargs)
        self.fields['recipient_arrival_date'].required = True
        self.fields['recipient_start_discharge_date'].required = True
        self.fields['recipient_end_discharge_date'].required = True
        
    class Meta:
        model = ets_models.Waybill
        fields = (
            'recipient_arrival_date',
            'recipient_start_discharge_date',
            'recipient_end_discharge_date',
            'recipient_distance',
            'recipient_remarks',
            'recipient_signed_date',
            'transport_delivery_signed_date',
            'container_one_remarks_reciept',
            'container_two_remarks_reciept',
        )


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


class LoadingDetailRecieptForm( ModelForm ):
    class Meta:
        model = ets_models.LoadingDetail
        fields = ( 
            'number_of_units', 'number_units_good', 
            'number_units_lost', 'number_units_damaged', 'units_lost_reason', 
            'units_damaged_reason', 
        )

