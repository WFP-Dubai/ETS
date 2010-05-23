from django.db import models
from django.contrib import admin

# Create your models here.
class Commodity(models.Model):
	commodityRef=models.TextField()
	commodityName=models.TextField()
	commodityType=models.TextField()
	def __unicode__(self):
		return self.commodityName
	
class CommodityAdmin(admin.ModelAdmin):
	list_display = ('commodityRef', 'commodityName', 'commodityType')
	
	
class LTI(models.Model): 
	LTI_ID=models.CharField(max_length=25)
	CODE=models.CharField(max_length=25)
	LTI_DATE=models.DateTimeField()
	CONTRACT_CODE=models.CharField(max_length=20)
	EXPIRY_DATE=models.DateTimeField()
	ORIGIN_TYPE=models.CharField(max_length=1)	
	ORIGIN_LOCATION_CODE=models.CharField(max_length=10)
	INTVYG_CODE=models.CharField(max_length=25)
	INTDLV_CODE=models.DecimalField( max_digits=2, decimal_places=0)
	ORIGIN_CODE=models.CharField(max_length=13)
	ORIGIN_DESCR=models.CharField(max_length=50)
	DESTINATION_LOCATION_CODE=models.CharField(max_length=10)
	ORGANIZATION_ID	=models.CharField(max_length=12)
	REQUESTED_DISPATCH_DATE=models.DateTimeField()
	INSPECTION_INDICATOR=models.CharField(max_length=1)
	OFFICER_CODE=models.CharField(max_length=7)
	PERSON2_OUC=models.CharField(max_length=13)
	TITLE_OF_OFFICER=models.CharField(max_length=50)
	ISSUING_CODE=models.CharField(max_length=7)
	PERSON1_OUC=models.CharField(max_length=13)
	TITLE_OF_ISSUING=models.CharField(max_length=50)
	TRANSPORTER_CODE=models.CharField(max_length=4)
	SUPPLIER_OUC=models.CharField(max_length=13)
	TRANSPORT_RATE_TYPE=models.CharField(max_length=10)
	TRANSPORT_CURRENCY=models.CharField(max_length=3)
	TRANSPORT_RATE=models.DecimalField(max_digits=15, decimal_places=3)
	FUEL_ENTITLEMENT=models.DecimalField( max_digits=15, decimal_places=3)
	FUEL_RATE=models.DecimalField( max_digits=15, decimal_places=3)
	FUEL_CURRENCY=models.CharField(max_length=3)
	FOOD_RELEASE=models.CharField(max_length=6)
	REMARKS	=models.CharField(max_length=250)
	REMARKS_B=models.CharField(max_length=250)
	OBSERVATIONS=models.CharField(max_length=250)
	STATUS_INDICATOR=models.CharField(max_length=1)
	ORG_UNIT_CODE=models.CharField(max_length=13)
	PRINTED_INDICATOR=models.CharField(max_length=1)
	OFFID=models.CharField(max_length=13)
	SEND_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	RECV_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	LAST_MOD_USER=models.CharField(max_length=30)
	LAST_MOD_DATE=models.DateTimeField()
	
	def  __unicode__(self):
		return self.LTI_ID + ' - ' + self.DESTINATION_LOCATION_CODE
	def mydesc(self):
		return self.LTI_ID + ' - ' + self.DESTINATION_LOCATION_CODE
class LTIAdmin(admin.ModelAdmin):
	list_display = ('LTI_ID', 'DESTINATION_LOCATION_CODE')
	
	
class LTIDetail(models.Model):
	OriginLTI=models.ForeignKey(LTI)
	SI_RECORD_ID=models.CharField(max_length=25)
	COMM_CATEGORY_CODE=models.CharField(max_length=9)
	COMMODITY_CODE=models.CharField(max_length=18)
	QUANTITY_NET=models.DecimalField( max_digits=11, decimal_places=3)
	QUANTITY_GROSS=models.DecimalField( max_digits=11, decimal_places=3)
	NUMBER_OF_UNITS=models.DecimalField( max_digits=7, decimal_places=0)
	UNIT_WEIGHT_NET=models.DecimalField( max_digits=8, decimal_places=3)
	UNIT_WEIGHT_GROSS=models.DecimalField( max_digits=8, decimal_places=3)
	OFFID=models.CharField(max_length=13)
	SEND_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	RECV_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	LAST_MOD_USER=models.CharField(max_length=20)
	LAST_MOD_DATE=models.DateTimeField()
	def  __unicode__(self):
		return self.OriginLTI.mydesc() + ' - ' + self.SI_RECORD_ID + ' - ' 
	def mydesc(self):
		return self.OriginLTI.mydesc() + ' - ' + self.SI_RECORD_ID + ' - ' 
	

class LTIDetailAdmin(admin.ModelAdmin):
	list_display = ('OriginLTI', 'SI_RECORD_ID')

class Waybill(models.Model):
	transaction_type_choice=(
			(u'INT', u'WFP Internal'),
			(u'DIS', u'Distribution'),
			(u'LON', u'Loan'),
			(u'DSP', u'Disposal'),
			(u'PUR', u'Purchase'),
			(u'SHU',u'Shunting'),
			(u'COS',u'Costal Transshipment'),
			(u'DEL',u'Delivery'),
			(u'SWA',u'Swap'),
			(u'REP',u'Repayment'),
			(u'SAL',u'Sale'),
			(u'ADR',u'Air drop'),
			(u'INL',u'Inland Shipment')
		)
	transport_type=(
			(u'R',u'Rail'),
			(u'T',u'Road'),
			(u'A',u'Air'),
			(u'I',u'Inland Waterways'),
			(u'C',u'Costal Waterways'),
			(u'M',u'Multi-mode'),
			(u'O',u'Other Please Specify')
		)
	#general
	ltiNumber=models.ForeignKey(LTI)
	waybillNumber=models.CharField(max_length=20)
	dateOfLoading=models.DateTimeField(null=True, blank=True)
	dateOfDispach=models.DateTimeField(null=True, blank=True)
	transactionType=models.CharField(max_length=10,choices=transaction_type_choice)
	transportType=models.CharField(max_length=10,choices=transport_type)
	#Dispatcher
	dispatchRemarks=models.TextField(blank=True)
	dispatcherName=models.TextField(blank=True)
	dispatcherTitle=models.TextField(blank=True)
	dispatcherSigned=models.BooleanField(blank=True)
	#Transporter
	transportContractor=models.TextField(blank=True)
	transportSubContractor=models.TextField(blank=True)
	transportDriverName=models.TextField(blank=True)
	transportDriverLicenceID=models.TextField(blank=True)
	transportVehicleRegistration=models.TextField(blank=True)
	transportTrailerRegistration=models.TextField(blank=True)
	containerOneSerialNumber=models.TextField(blank=True)
	containerTwoSerialNumber=models.TextField(blank=True)
	transportDispachSigned=models.BooleanField(blank=True)
	transportDeliverySigned=models.BooleanField(blank=True)
	#Reciver
	recipientLocation=models.TextField(blank=True)
	recipientConsingee=models.TextField(blank=True)
	recipientName=models.TextField(blank=True)
	recipientTitle=models.TextField(blank=True)
	recipientArrivalDate=models.TextField(blank=True)
	recipientStartDischargeDate=models.TextField(blank=True)
	recipientEndDischargeDate=models.TextField(blank=True)
	recipientDistance=models.TextField(blank=True)
	recipientRemarks=models.TextField(blank=True)
	recipientSigned=models.BooleanField(blank=True)
	#Extra Fields
	waybillValidated=models.BooleanField()
	waybillProcessedForPayment=models.BooleanField()
	def  __unicode__(self):
		return self.waybillNumber
	def mydesc(self):
		return self.waybillNumber
class WaybillAdmin(admin.ModelAdmin):
	list_display=('waybillNumber','ltiNumber')

class LoadingDetail(models.Model):
	wbNumber=models.ForeignKey(Waybill)
	siNo=models.ForeignKey(LTIDetail)
	commodity=models.ForeignKey(Commodity)
	numberUnitsLoaded=models.IntegerField(blank=True)
	numberUnitsGood=models.IntegerField(blank=True)
	numberUnitsLost=models.IntegerField(blank=True)
	numberUnitsDamaged=models.IntegerField(blank=True)
	unitsLostReason=models.TextField(blank=True)
	unitsDamagedReason=models.TextField(blank=True)
	def  __unicode__(self):
		return self.wbNumber.mydesc() +' - '+ self.siNo.mydesc()
	

	
	
	
admin.site.register(Commodity,CommodityAdmin)
admin.site.register(LTI,LTIAdmin)
admin.site.register(Waybill,WaybillAdmin)
admin.site.register(LoadingDetail)
admin.site.register(LTIDetail,LTIDetailAdmin)

