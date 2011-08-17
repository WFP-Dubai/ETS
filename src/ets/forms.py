import datetime

from django.forms.models import  BaseModelFormSet, BaseInlineFormSet
from django.forms.formsets import formset_factory, BaseFormSet
from django import forms
#from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext, ugettext_lazy as _

from uni_form.helpers import FormHelper, Layout, Fieldset, Row, HTML

from ets import models as ets_models

UNDEFINED_MESSAGE = "N/A"

class WarehouseChoiceForm( forms.Form ):
    warehouse = forms.ModelChoiceField( queryset = ets_models.Warehouse.objects.filter( start_date__lt = datetime.date.today() ) )

class WaybillSearchForm( forms.Form ):
    q = forms.CharField(required=False, label=_('Waybill code'))


class DispatchWaybillForm( forms.ModelForm ):
    
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
        Fieldset(ugettext('Date'), Row('loading_date', 'dispatch_date')),
        Fieldset(ugettext('General'),
                'destination',
                Row('transaction_type', 'transport_type'),
                'dispatch_remarks',
                 ),
        Fieldset(ugettext('Transport'),
                 'transport_sub_contractor',
                 Row('transport_driver_name', 'transport_driver_licence'),
                 Row('transport_vehicle_registration', 'transport_trailer_registration'),
                 ),
        Fieldset(ugettext('Container'),
                 Row('container_one_number', 'container_one_seal_number', 'container_one_remarks_dispatch'),
                 Row('container_two_number', 'container_two_seal_number', 'container_two_remarks_dispatch'),
                 )
    ))
                      
    #helper.add_input(Submit('add', _('Create waybill')))
    helper.form_tag = False


class LoadingDetailDispatchForm( forms.ModelForm ):
    stock_item = forms.ModelChoiceField(queryset=ets_models.StockItem.objects.all(), 
                                        label=_('Commodity'), required=True)
    overload = forms.BooleanField( required = False )

    class Meta:
        model = ets_models.LoadingDetail
        fields = ( 'number_of_units', 'overloaded_units', 'over_offload_units' )
    
    def save(self, commit=True):
        obj = super(LoadingDetailDispatchForm, self).save(commit=False)
        stock_item = self.cleaned_data.get('stock_item')
        if stock_item:
            obj.origin_id = stock_item.pk
            obj.si_code = stock_item.si_code
            
            obj.comm_category_code = stock_item.comm_category_code
            obj.commodity_code = stock_item.commodity_code
            obj.commodity_name = stock_item.commodity_name
            
            obj.unit_weight_net = stock_item.unit_weight_net
            obj.unit_weight_gross = stock_item.unit_weight_gross
            
            obj.package = stock_item.packaging_description()
        
        if commit:
            obj.save()
        
        return obj


class BaseLoadingDetailFormFormSet(BaseModelFormSet):
    
#    def append_non_form_error( self, message ):
#        errors = super( BaseLoadingDetailFormFormSet, self ).non_form_errors()
#        errors.append( message )
#        raise forms.ValidationError( errors )
    
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
                                 'over_offload_units', 'overload',)))
    helper.formset_tag = False


class WaybillRecieptForm( forms.ModelForm ):
    
    required_fields = (
        'recipient_arrival_date', 
        'recipient_start_discharge_date', 
        'recipient_end_discharge_date',
        )
    
    def __init__(self, **kwargs):
        super(WaybillRecieptForm, self).__init__(**kwargs)
        for field_name in self.required_fields:
            self.fields[field_name].required = True
        
    class Meta:
        model = ets_models.Waybill
        fields = (
            'recipient_arrival_date',
            'recipient_start_discharge_date',
            'recipient_end_discharge_date',
            'recipient_distance',
            'recipient_remarks',
            #'recipient_signed_date',
            #'transport_delivery_signed_date',
            'container_one_remarks_reciept',
            'container_two_remarks_reciept',
        )
    
    helper = FormHelper()
    
    # create the layout object
    helper.add_layout(Layout(
        Fieldset(ugettext('Dates'), Row('recipient_arrival_date', 'recipient_start_discharge_date', 'recipient_end_discharge_date')),
        Fieldset(ugettext('Containers'), Row('container_one_remarks_reciept', 'container_two_remarks_reciept')),
        Fieldset('', Row('recipient_distance', 'recipient_remarks')),
    ))
    
    helper.form_tag = False


class LoadingDetailRecieptForm( forms.ModelForm ):
    
    def __init__(self, *args, **kwargs):
        super(LoadingDetailRecieptForm, self).__init__(*args, **kwargs)
        
        for field_name in ('units_lost_reason', 'units_damaged_reason'):
            self.fields[field_name].queryset = self.fields[field_name].queryset.filter(comm_category_code=self.instance.comm_category_code)
        
    
    class Meta:
        model = ets_models.LoadingDetail
        fields = (
            'origin_id', 'commodity_name',
            'number_units_good', 
            'number_units_lost', 'units_lost_reason',
            'number_units_damaged', 'units_damaged_reason',
        )
        widgets = {
            'number_units_good': forms.TextInput(attrs={'size': 5}),
            'number_units_lost': forms.TextInput(attrs={'size': 5}),
            'number_units_damaged': forms.TextInput(attrs={'size': 5}),
        }


class BaseRecieptFormFormSet(BaseInlineFormSet):
    
    helper = FormHelper()
    
    # create the layout object
    helper.add_layout(Layout(
        #HTML('<strong>{{ form.instance.origin_id }}</strong> <strong>{{ form.instance.commodity_name }}</strong>'),
        Row(
        'origin_id', 'commodity_name', 'number_units_good', 
        'number_units_lost', 'units_lost_reason',
        'number_units_damaged', 'units_damaged_reason',
    )))
    helper.formset_tag = False


class WaybillFullForm( forms.ModelForm ):

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
