from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from ets.waybill.views import *
from ets.waybill.models import *
from django import forms
from django.forms.extras.widgets import SelectDateWidget

class WaybillForm(ModelForm):

	dateOfLoading = forms.DateField()
	dateOfDispatch = forms.DateField()
	transportType = forms.CharField(widget=forms.RadioSelect(choices=Waybill.transport_type))
	transactionType = forms.CharField(widget=forms.RadioSelect(choices=Waybill.transaction_type_choice))
	dispatchRemarks=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	ltiNumber = forms.CharField(widget=forms.HiddenInput())
	transportContractor = forms.CharField(widget=forms.HiddenInput())
	transportSubContractor=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	transportDriverName=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	transportDriverLicenceID=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	transportVehicleRegistration=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	dispatcherName = forms.CharField(widget=forms.HiddenInput(),required=False)
	dispatcherTitle= forms.CharField(widget=forms.HiddenInput(),required=False)
	transportTrailerRegistration=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	recipientLocation = forms.CharField(widget=forms.HiddenInput())
	recipientConsingee = forms.CharField(widget=forms.HiddenInput())
	waybillNumber = forms.CharField(widget=forms.HiddenInput())
	destinationWarehouse= ModelChoiceField(queryset=places.objects.all())	
	
	
        
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
        	]
        	

class WaybillRecieptForm(ModelForm):
	recipientArrivalDate = forms.DateField()
	recipientStartDischargeDate = forms.DateField()
	recipientEndDischargeDate = forms.DateField()
	waybillNumber = forms.CharField(widget=forms.HiddenInput())
	recipientLocation = forms.CharField(widget=forms.HiddenInput())
	recipientRemarks=forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	recipientConsingee = forms.CharField(widget=forms.HiddenInput())
	
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
				'containerTwoRemarksReciept'
			]

class WaybillFullForm(ModelForm):
	
	dateOfDispatch 					= forms.DateField(required=False)
	dateOfLoading 					= forms.DateField(required=False)
	dispatchRemarks					= forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)

	recipientArrivalDate 			= forms.DateField(required=False)
	recipientEndDischargeDate 		= forms.DateField(required=False)
	recipientRemarks				= forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	recipientStartDischargeDate 	= forms.DateField(required=False)
	transactionType 				= forms.CharField(widget=forms.RadioSelect(choices=Waybill.transaction_type_choice))
	transportDriverLicenceID		= forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	transportDriverName				= forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	transportSubContractor			= forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	transportTrailerRegistration	= forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	transportType 					= forms.CharField(widget=forms.RadioSelect(choices=Waybill.transport_type))
	transportVehicleRegistration	= forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
	recipientLocation 				= forms.CharField(widget=forms.HiddenInput(),required=False)
	recipientConsingee 				= forms.CharField(widget=forms.HiddenInput(),required=False)
	ltiNumber 						= forms.CharField(widget=forms.HiddenInput(),required=False)
	transportContractor 			= forms.CharField(widget=forms.HiddenInput(),required=False)	
	waybillNumber					= forms.CharField(widget=forms.HiddenInput(),required=False)
	recipientConsingee				= forms.CharField(widget=forms.HiddenInput(),required=False)
	recipientName					= forms.CharField(widget=forms.HiddenInput(),required=False)
	recipientTitle					= forms.CharField(widget=forms.HiddenInput(),required=False)
	recipientSignedTimestamp		= forms.DateTimeField(widget=forms.HiddenInput(),required=False)
	transportDispachSigned			= forms.CharField(widget=forms.HiddenInput(),required=False)
	transportDispachSignedTimestamp	= forms.DateTimeField(widget=forms.HiddenInput(),required=False)
	transportDeliverySigned			= forms.CharField(widget=forms.HiddenInput(),required=False)
	transportDeliverySignedTimestamp= forms.DateTimeField(widget=forms.HiddenInput(),required=False)
	dispatcherName					= forms.CharField(widget=forms.HiddenInput(),required=False)
	dispatcherTitle					= forms.CharField(widget=forms.HiddenInput(),required=False)

	class Meta:
		model=Waybill
	
	def thisDispName(self):
		try:
			name = EpicPerson.objects.get(person_pk=self.instance.dispatcherName)
		except:
			name = 'N/A'
		return name
	def thisRecName(self):
		try:
			name = EpicPerson.objects.get(person_pk=self.instance.recipientName)
		except:
			name = 'N/A'
		return name

		
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - %s" % (obj.SI_CODE , obj.CMMNAME )

class LoadingDetailDispatchForm(ModelForm):
	class Meta:
		model = LoadingDetail
		fields = ('siNo','numberUnitsLoaded')

class LoadingDetailRecieptForm(ModelForm):
	class Meta:
		model = LoadingDetail
		fields = ('siNo','numberUnitsLoaded','numberUnitsGood','numberUnitsLost','numberUnitsDamaged','unitsLostReason','unitsDamagedReason',)
