from django.db import models, connection
from django.contrib import admin
from django.forms import ModelForm

# Create your models here.
class Commodity(models.Model):
	commodityRef=models.CharField(max_length=18)
	commodityName=models.CharField(max_length=100)
	commodityType=models.CharField(max_length=9)
	def __unicode__(self):
		return self.commodityRef +' - ' + self.commodityName
	
class CommodityAdmin(admin.ModelAdmin):
	list_display = ('commodityRef', 'commodityName', 'commodityType')



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
	ltiNumber				=models.CharField(max_length=20)
	waybillNumber			=models.CharField(max_length=20)
	dateOfLoading			=models.DateField(null=True, blank=True)
	dateOfDispach			=models.DateField(null=True, blank=True)
	transactionType			=models.CharField(max_length=10,choices=transaction_type_choice)
	transportType			=models.CharField(max_length=10,choices=transport_type)
	#Dispatcher
	dispatchRemarks			=models.TextField(blank=True)
	dispatcherName			=models.TextField(blank=True)
	dispatcherTitle			=models.TextField(blank=True)
	dispatcherSigned		=models.BooleanField(blank=True)
	#Transporter
	transportContractor		=models.TextField(blank=True)
	transportSubContractor		=models.TextField(blank=True)
	transportDriverName		=models.TextField(blank=True)
	transportDriverLicenceID	=models.TextField(blank=True)
	transportVehicleRegistration	=models.TextField(blank=True)
	transportTrailerRegistration	=models.TextField(blank=True)
	transportDispachSigned		=models.BooleanField(blank=True)
	transportDispachSignedTimestamp	=models.DateTimeField(null=True, blank=True)
	transportDeliverySigned		=models.BooleanField(blank=True)
	transportDeliverySignedTimestamp=models.DateTimeField(null=True, blank=True)
	
	#Container	
	containerOneNumber		=models.CharField(max_length=40,blank=True)
	containerTwoNumber		=models.CharField(max_length=40,blank=True)
	containerOneSealNumber		=models.CharField(max_length=40,blank=True)
	containerTwoSealNumber		=models.CharField(max_length=40,blank=True)


	#Reciver
	recipientLocation		=models.CharField(max_length=100,blank=True)
	recipientConsingee		=models.CharField(max_length=100,blank=True)
	recipientName			=models.CharField(max_length=100,blank=True)
	recipientTitle			=models.CharField(max_length=100,blank=True)
	recipientArrivalDate		=models.DateField(null=True, blank=True)
	recipientStartDischargeDate	=models.DateField(null=True, blank=True)
	recipientEndDischargeDate	=models.DateField(null=True, blank=True)
	recipientDistance		=models.IntegerField(blank=True,null=True)
	recipientRemarks		=models.TextField(blank=True)
	recipientSigned			=models.BooleanField(blank=True)
	recipientSignedTimestamp	=models.DateTimeField(null=True, blank=True)
	
	#Extra Fields
	waybillValidated		=models.BooleanField()
	waybillProcessedForPayment	=models.BooleanField()
	def  __unicode__(self):
		return self.waybillNumber
	def mydesc(self):
		return self.waybillNumber

	
#### CPS DB

class ltioriginalManager(models.Manager):
	def warehouses(self):
		cursor = connection.cursor()
		cursor.execute("""
		    SELECT DISTINCT ORIGIN_LOCATION_CODE,ORIGIN_LOC_NAME,ORIGIN_WH_NAME
		    FROM epic_lti
		    """)
		wh = cursor.fetchall()
		return wh
	def ltiCodes(self):
		cursor = connection.cursor()
		cursor.execute("""
		    SELECT DISTINCT CODE
		    FROM epic_lti order by LTI_ID
		    """)
		lti_code = cursor.fetchall()
		return lti_code
		

class ltioriginal(models.Model):
	LTI_PK				=models.CharField(max_length=50, primary_key=True)
	LTI_ID				=models.CharField(max_length=40)
	CODE            		=models.CharField(max_length=40)
	LTI_DATE			=models.DateField()
	EXPIRY_DATE			=models.DateField(blank=True,null=True)
	TRANSPORT_CODE			=models.CharField(max_length=4)
	TRANSPORT_OUC			=models.CharField(max_length=13)
	TRANSPORT_NAME			=models.CharField(max_length=30)
	ORIGIN_TYPE			=models.CharField(max_length=1)
	ORIGINTYPE_DESC         	=models.CharField(max_length=12,blank=True)
	ORIGIN_LOCATION_CODE		=models.CharField(max_length=10)
	ORIGIN_LOC_NAME			=models.CharField(max_length=30)
	ORIGIN_WH_CODE			=models.CharField(max_length=13,blank=True)
	ORIGIN_WH_NAME			=models.CharField(max_length=50,blank=True)
	DESTINATION_LOCATION_CODE	=models.CharField(max_length=10)
	DESTINATION_LOC_NAME		=models.CharField(max_length=30)
	CONSEGNEE_CODE			=models.CharField(max_length=12)
	CONSEGNEE_NAME			=models.CharField(max_length=80)
	REQUESTED_DISPATCH_DATE		=models.DateField(blank=True,null=True)
	PROJECT_WBS_ELEMENT		=models.CharField(max_length=24,blank=True)
	SI_RECORD_ID			=models.CharField(max_length=25,blank=True)
	SI_CODE				=models.CharField(max_length=8)
	COMM_CATEGORY_CODE		=models.CharField(max_length=9)
	COMMODITY_CODE			=models.CharField(max_length=18)
	CMMNAME				=models.CharField(max_length=100,blank=True)
	QUANTITY_NET			=models.DecimalField(max_digits=11, decimal_places=3)
	QUANTITY_GROSS			=models.DecimalField(max_digits=11, decimal_places=3)
	NUMBER_OF_UNITS			=models.DecimalField(max_digits=7, decimal_places=0)
	UNIT_WEIGHT_NET			=models.DecimalField(max_digits=8, decimal_places=3,blank=True,null=True)
	UNIT_WEIGHT_GROSS		=models.DecimalField(max_digits=8, decimal_places=3,blank=True,null=True)
	
	objects = ltioriginalManager()
	class Meta:
		db_table = u'epic_lti'
	def  __unicode__(self):
		return self.CODE +' - '+ self.SI_CODE

####


class LoadingDetail(models.Model):
	wbNumber				=models.ForeignKey(Waybill)
	siNo					=models.ForeignKey(ltioriginal)
	numberUnitsLoaded		=models.IntegerField(blank=True)
	numberUnitsGood			=models.IntegerField(blank=True)
	numberUnitsLost			=models.IntegerField(blank=True)
	numberUnitsDamaged		=models.IntegerField(blank=True)
	unitsLostReason			=models.TextField(blank=True)
	unitsDamagedReason		=models.TextField(blank=True)
	def  __unicode__(self):
		return self.wbNumber.mydesc() +' - '+ self.siNo.mydesc()
		
class LoadingDetailInline(admin.TabularInline):
	model = LoadingDetail

class WaybillAdmin(admin.ModelAdmin):
	list_display=('waybillNumber','ltiNumber')
	inlines = [LoadingDetailInline]

class LoadingDetailAdmin(admin.ModelAdmin):
	list_display=('waybillNumber','siNo')

class ltioriginalAdmin(admin.ModelAdmin):
	list_display=('CODE','SI_CODE')
	
class WaybillForm(ModelForm):
     class Meta:
         model = Waybill

admin.site.register(Commodity,CommodityAdmin)
admin.site.register(Waybill,WaybillAdmin)
admin.site.register(LoadingDetail)
admin.site.register(ltioriginal,ltioriginalAdmin)

