### -*- coding: utf-8 -*- ####################################################
from itertools import chain

from django.forms.models import BaseModelFormSet, BaseInlineFormSet
#from django.forms.formsets import formset_factory, BaseFormSet
from django.contrib.auth.forms import UserChangeForm
from django import forms
#from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from uni_form.helper import FormHelper
from uni_form.layout import Layout, Fieldset, Row, Submit

from ets import models as ets_models
from ets.utils import LOGENTRY_WAYBILL_ACTIONS, ACTION_TYPES

UNDEFINED_MESSAGE = "N/A"

class StrippedTextInput(forms.TextInput):
    """Special form input to strip spaces."""
    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.
        """
        value = data.get(name, None)
        if value is not None:
            value = value.strip()
        
        return value


class PersonChangeForm(UserChangeForm):
    """Person model form"""
    class Meta:
        model = ets_models.Person

class WaybillSearchForm( forms.Form ):
    """Search form with only one field: query set"""
    q = forms.CharField(required=True, label=_('eWaybill Code'))

class WaybillScanForm( forms.Form ):
    """Waybill scan form with one input"""
    data = forms.CharField(required=True, label=_('Scan eWaybill'))

class DispatchWaybillForm( forms.ModelForm ):
    """Dispatch waybill form."""
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
            'transport_driver_name': StrippedTextInput(),
            'transport_driver_licence': StrippedTextInput(),
            'transport_vehicle_registration': StrippedTextInput(),
        }
    
    helper = FormHelper()
    
    # create the layout object
    helper.add_layout(Layout(
        Fieldset(ugettext('Remarks'), 'dispatch_remarks'),
        Fieldset(ugettext('Dates'), Row('loading_date', 'dispatch_date')),
        Fieldset(ugettext('General'),
                'destination',
                Row('transaction_type', 'transport_type'),
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
    """LoadingDetails model form to use in dispatch page."""
    class Meta:
        model = ets_models.LoadingDetail
        fields = (
            'stock_item', 'number_of_units', 'overloaded_units', 
            'unit_weight_net', 'unit_weight_gross', 
            'total_weight_net', 'total_weight_gross',
        )
        widgets = {
            'number_of_units': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
            'unit_weight_net': forms.TextInput(attrs={'size': 5, 'class': 'unit-weight-net'}),
            'unit_weight_gross': forms.TextInput(attrs={'size': 5, 'class': 'unit-weight-gross'}),
            'total_weight_net': forms.TextInput(attrs={'size': 5, 'class': 'weight-total-net'}),
            'total_weight_gross': forms.TextInput(attrs={'size': 5, 'class': 'weight-total-gross'}),
        }

class BaseLoadingDetailFormSet(BaseInlineFormSet):
    """FormSet base model. We use this formset in dispatch page."""
    
    def clean(self):
        """Validates number of waybill items. System requires at least one line."""
        super(BaseLoadingDetailFormSet, self).clean()
        count = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            if form.is_bound and getattr(form, 'cleaned_data', {}).get('number_of_units'):
                count += 1
            
        if count < 1:
            raise forms.ValidationError( _('You must have at least one loading detail with no issues') )
    

class WaybillRecieptForm( forms.ModelForm ):
    """Waybill receipt form."""
    
    def __init__(self, *args, **kwargs):
        """ Makes date fields required """
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
        Fieldset(ugettext('Destination'), 'receipt_remarks', Row('destination', 'distance')),
        Fieldset(ugettext('Dates'), Row('arrival_date', 'start_discharge_date', 'end_discharge_date')),
        Fieldset(ugettext('Containers'), 
                 Row('container_one_remarks_reciept', 'container_two_remarks_reciept'),),
    ))
    
    helper.form_tag = False


class LoadingDetailReceiptForm( forms.ModelForm ):
    """Model form for loading details on receipt page."""
    
    def __init__(self, *args, **kwargs):
        """Filters loss and damage reason choice."""
        super(LoadingDetailReceiptForm, self).__init__(*args, **kwargs)
        
        for field_name in ('units_lost_reason', 'units_damaged_reason'):
            self.fields[field_name].queryset = self.fields[field_name].queryset.filter(category=self.instance.stock_item.commodity.category)
    
    def clean(self):
        """Validates entered values, i.e. quantities"""
        super(LoadingDetailReceiptForm, self).clean()
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
            'total_weight_net_received',
            'total_weight_gross_received',
            'over_offload_units',
        )
        widgets = {
            'number_units_good': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
            'number_units_lost': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
            'number_units_damaged': forms.TextInput(attrs={'size': 5, 'class': 'number'}),
        }
        

class ImportDataForm( forms.Form ):
    """Form that accepts file to import datas."""
    file = forms.FileField(required=True, label=_('Import Data'))

    helper = FormHelper()
    helper.add_input(Submit(_("Submit"), 'submit'))

class WaybillActionForm( forms.Form ):
    WAYBILL_ACTIONS = chain(((0, " - - - - - -"),), ACTION_TYPES)
    action_type = forms.TypedChoiceField(choices=WAYBILL_ACTIONS, coerce=lambda val: int(val), required=True)
