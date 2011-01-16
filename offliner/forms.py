'''
Created on 02/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.forms.models import  BaseModelFormSet

from offliner.models import Waybill, Places, EpicPerson, LoadingDetail


class WaybillForm(ModelForm):
    '''
    WaybillForm #@todo: write Class definition
    '''
    dateOfLoading = forms.DateField()
    dateOfDispatch = forms.DateField()
    transportType = forms.CharField(widget=forms.RadioSelect(choices=Waybill.transport_type))
    transactionType = forms.CharField(widget=forms.RadioSelect(choices=Waybill.transaction_type_choice))
    dispatchRemarks = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    ltiNumber = forms.CharField(widget=forms.HiddenInput())
    transportContractor = forms.CharField(widget=forms.HiddenInput())
    transportSubContractor = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    transportDriverName = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    transportDriverLicenceID = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    transportVehicleRegistration = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    dispatcherName = forms.CharField(widget=forms.HiddenInput(), required=False)
    dispatcherTitle = forms.CharField(widget=forms.HiddenInput(), required=False)
    transportTrailerRegistration = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    recipientLocation = forms.CharField(widget=forms.HiddenInput())
    recipientConsingee = forms.CharField(widget=forms.HiddenInput())
    waybillNumber = forms.CharField(widget=forms.HiddenInput())
    destinationWarehouse = forms.ModelChoiceField(queryset=Places.objects.all())    
    invalidated = forms.CharField(widget=forms.HiddenInput(), required=False)
    auditComment = forms.CharField(widget=forms.HiddenInput(), required=False)
            
    class Meta:
        model = Waybill
        fields = [
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
        ]
        
    def clean(self):
        cleaned = self.cleaned_data
        dateOfDispatch = cleaned.get('dateOfDispatch')
        dateOfLoading = cleaned.get('dateOfLoading')

        faults = False
        myerror = ''
        if dateOfLoading > dateOfDispatch:
            myerror = ''
            myerror = "Cargo Dispatched before being Loaded"
            self._errors['dateOfDispatch'] = self._errors.get('dateOfDispatch', [])
            self._errors['dateOfDispatch'].append(myerror)
            faults = True
    
        if faults:
            raise forms.ValidationError(myerror)

        return cleaned


class WaybillRecieptForm(ModelForm):
    '''
    WaybillRecieptForm #@todo: write Class definition
    '''    
    recipientArrivalDate = forms.DateField()
    recipientStartDischargeDate = forms.DateField()
    recipientEndDischargeDate = forms.DateField()
    waybillNumber = forms.CharField(widget=forms.HiddenInput())
    recipientLocation = forms.CharField(widget=forms.HiddenInput())
    recipientRemarks = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    recipientConsingee = forms.CharField(widget=forms.HiddenInput())
    invalidated = forms.CharField(widget=forms.HiddenInput(), required=False)    
    auditComment = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Waybill
        fields = [
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
            ]
        
    def clean(self):
        cleaned = self.cleaned_data
        dispatch_date = self.instance.dateOfDispatch
        arrival_date = cleaned.get('recipientArrivalDate')
        discharge_start = cleaned.get('recipientStartDischargeDate')
        discharge_end = cleaned.get('recipientEndDischargeDate')
        faults = False
        
        if arrival_date < dispatch_date:
            myerror = ''
            myerror = "Cargo arrived before being dispatched"
            self._errors['recipientArrivalDate'] = self._errors.get('recipientArrivalDate', [])
            self._errors['recipientArrivalDate'].append(myerror)
            faults = True
        
        if discharge_start < arrival_date:
            myerror = ''
            myerror = "Cargo Discharge started before Arrival?"
            self._errors['recipientStartDischargeDate'] = self._errors.get('recipientStartDischargeDate', [])
            self._errors['recipientStartDischargeDate'].append(myerror)
            faults = True        
        
        if discharge_end < discharge_start:
            myerror = ''
            myerror = "Cargo finished Discharge before Starting?"
            self._errors['recipientEndDischargeDate'] = self._errors.get('recipientEndDischargeDate', [])
            self._errors['recipientEndDischargeDate'].append(myerror)
            faults = True
        
        if faults:
            raise forms.ValidationError(myerror)

        return cleaned


#class WaybillFullForm(ModelForm):
#    '''
#    WaybillFullForm #@todo: write Class definition
#    '''
#    dateOfDispatch = forms.DateField(required=False)
#    dateOfLoading = forms.DateField(required=False)
#    dispatchRemarks = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
#    dispatcherName = forms.CharField(widget=forms.HiddenInput(), required=False)
#    dispatcherTitle = forms.CharField(widget=forms.HiddenInput(), required=False)
#    invalidated = forms.CharField(widget=forms.HiddenInput(), required=False)
#    ltiNumber = forms.CharField(widget=forms.HiddenInput(), required=False)
#    recipientArrivalDate = forms.DateField(required=False)
#    recipientConsingee = forms.CharField(widget=forms.HiddenInput(), required=False)
#    recipientConsingee = forms.CharField(widget=forms.HiddenInput(), required=False)
#    recipientEndDischargeDate = forms.DateField(required=False)
#    recipientLocation = forms.CharField(widget=forms.HiddenInput(), required=False)
#    recipientName = forms.CharField(widget=forms.HiddenInput(), required=False)
#    recipientRemarks = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
#    recipientSignedTimestamp = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
#    recipientStartDischargeDate = forms.DateField(required=False)
#    recipientTitle = forms.CharField(widget=forms.HiddenInput(), required=False)
#    transactionType = forms.CharField(widget=forms.RadioSelect(choices=Waybill.transaction_type_choice))
#    transportContractor = forms.CharField(widget=forms.HiddenInput(), required=False)
#    transportDeliverySigned = forms.CharField(widget=forms.HiddenInput(), required=False)
#    transportDeliverySignedTimestamp = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
#    transportDispachSigned = forms.CharField(widget=forms.HiddenInput(), required=False)
#    transportDispachSignedTimestamp = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
#    transportDriverLicenceID = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
#    transportDriverName = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
#    transportSubContractor = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
#    transportTrailerRegistration = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
#    transportType = forms.CharField(widget=forms.RadioSelect(choices=Waybill.transport_type))
#    transportVehicleRegistration = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
#    waybillNumber = forms.CharField(widget=forms.HiddenInput(), required=False)
#    auditComment = forms.CharField(widget=forms.Textarea, required=True)
#
#    class Meta:
#        model = Waybill
#
#    def thisDispName(self):
#        try:
#            name = EpicPerson.objects.get(person_pk=self.instance.dispatcherName)
#        except:
#            name = 'N/A'
#        return name
#
#    def thisRecName(self):
#        try:
#            name = EpicPerson.objects.get(person_pk=self.instance.recipientName)
#        except:
#            name = 'N/A'
#        return name


#class WaybillValidationFormset(BaseModelFormSet):
#    '''
#    WaybillValidationFormset #@todo: write Class definition
#    '''
#
#    def clean(self):
#        super(WaybillValidationFormset, self).clean()
#        # example custom validation across forms in the formset:
#        issue = ''
#        for form in self.forms:
#            if form.check_lines():
#                pass
#            else:
#                valid = False
#                issue += ' WB: ' + str(form)
#                raise form.ValidationError("You have an error")
#            if valid:
#                pass#formset.save()
#            else:
#                print issue
 
    
class MyModelChoiceField(forms.ModelChoiceField):
    '''
    MyModelChoiceField #@todo: write Class definition
    '''  
        
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.si_code , obj.cmmname)
    

class LoadingDetailDispatchForm(ModelForm):
    '''
    LoadingDetailDispatchForm #@todo: write Class definition
    '''  
        
    class Meta:
        model = LoadingDetail
        fields = ('siNo', 'numberUnitsLoaded')


class LoadingDetailRecieptForm(ModelForm):
    '''
    LoadingDetailRecieptForm #@todo: write Class definition
    ''' 
        
    class Meta:
        model = LoadingDetail
        fields = ('siNo', 'numberUnitsLoaded', 'numberUnitsGood', 'numberUnitsLost', 'numberUnitsDamaged', 'unitsLostReason', 'unitsDamagedReason',)
    
        
class ImportFileForm(forms.Form):
    file = forms.FileField()  
    
         
