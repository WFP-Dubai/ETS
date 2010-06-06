from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from ets.waybill.views import *
from ets.waybill.models import *


class WaybillForm(ModelForm):

     class Meta:
        model = Waybill
        fields = [
        	
        	'waybillNumber',
        	'dateOfLoading',
         	'dateOfDispatch',
        	'transactionType',
        	'transportType',
        	'dispatchRemarks',
        	'dispatcherName',
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
        	'containerTwoSealNumber','recipientLocation' 	
        	]

class WaybillRecieptForm(ModelForm):
	
     class Meta:
        model = Waybill
        fields = ('waybillNumber',
'recipientLocation','recipientConsingee','recipientName',
'recipientTitle','recipientArrivalDate','recipientStartDischargeDate','recipientEndDischargeDate',
'recipientDistance','recipientRemarks','recipientSigned','recipientSignedTimestamp'
        	)


		
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
