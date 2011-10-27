### -*- coding: utf-8 -*- ####################################################

from django.forms.models import  BaseModelFormSet, BaseInlineFormSet
#from django.forms.formsets import formset_factory, BaseFormSet
from django.contrib.auth.forms import UserChangeForm
from django import forms
#from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext, ugettext_lazy as _

from uni_form.helper import FormHelper
from uni_form.layout import Layout, Fieldset, Row

from ets import models as ets_models

UNDEFINED_MESSAGE = "N/A"

class PersonChangeForm(UserChangeForm):
    class Meta:
        model = ets_models.Person

class WaybillSearchForm( forms.Form ):
    q = forms.CharField(required=True, label=_('Waybill code'))

class WaybillScanForm( forms.Form ):
    data = forms.CharField(required=True, label=_('Scan Waybill'))

class DispatchWaybillForm( forms.ModelForm ):
    
    class Meta:
        model = ets_models.Waybill
        fields = (
            'destination',
            'loading_date',
            'dispatch_date',
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
            'dispatch_remarks': forms.Textarea(attrs={'rows': "3"}),
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

    class Meta:
        model = ets_models.LoadingDetail
        fields = ( 'stock_item', 'number_of_units', 'overloaded_units' )
        widgets = {
            'number_of_units': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
        }

class BaseLoadingDetailFormSet(BaseInlineFormSet):
    
    def clean(self):
        super(BaseLoadingDetailFormSet, self).clean()
        count = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if form.is_bound and getattr(form, 'cleaned_data', {}).get('number_of_units'):
                count += 1
            
        if count < 1:
            raise forms.ValidationError( _('You must have at least one commodity') )
    

class WaybillRecieptForm( forms.ModelForm ):
    
    def __init__(self, *args, **kwargs):
        super(WaybillRecieptForm, self).__init__(*args, **kwargs)
        for field_name in ('arrival_date', 'start_discharge_date', 'end_discharge_date',):
            self.fields[field_name].required = True
    
    class Meta:
        model = ets_models.Waybill
        fields = (
            'destination',
            'receipt_remarks',
            'arrival_date',
            'start_discharge_date',
            'end_discharge_date',
            'distance',
            'container_one_remarks_reciept',
            'container_two_remarks_reciept',
        )
        widgets = {
            'receipt_remarks': forms.Textarea(attrs={'rows': "3"}),
            'distance': forms.TextInput(attrs={'size': 5, 'class': 'number'}),           
        }
    
    helper = FormHelper()
    
    # create the layout object
    helper.add_layout(Layout(
        Fieldset(ugettext('Destination'), Row('destination', 'distance')),
        Fieldset(ugettext('Dates'), Row('arrival_date', 'start_discharge_date', 'end_discharge_date')),
        Fieldset(ugettext('Remarks'), 'receipt_remarks', 
                 Row('container_one_remarks_reciept', 'container_two_remarks_reciept'),),
    ))
    
    helper.form_tag = False


class LoadingDetailRecieptForm( forms.ModelForm ):
    
    def __init__(self, *args, **kwargs):
        super(LoadingDetailRecieptForm, self).__init__(*args, **kwargs)
        
        for field_name in ('units_lost_reason', 'units_damaged_reason'):
            self.fields[field_name].queryset = self.fields[field_name].queryset.filter(category=self.instance.stock_item.commodity.category)
    
    def clean(self):
        super(LoadingDetailRecieptForm, self).clean()
        if hasattr(self, 'cleaned_data'):
            if not self.cleaned_data.get('number_units_good')\
                and not self.cleaned_data.get('number_units_damaged')\
                and not self.cleaned_data.get('number_units_lost'):
                raise forms.ValidationError(_("At least one of the fields number_units_good, number_units_damaged, number_units_lost must be filled"))
        return self.cleaned_data    

    class Meta:
        model = ets_models.LoadingDetail
        fields = (
            'number_units_good', 
            'number_units_lost', 'units_lost_reason',
            'number_units_damaged', 'units_damaged_reason',
            'over_offload_units',
        )
        widgets = {
            'number_units_good': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
            'number_units_lost': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
            'number_units_damaged': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
        }
