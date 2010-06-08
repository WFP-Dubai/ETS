from django.db import models, connection
from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory


# Create your models here.
class Commodity(models.Model):
	commodityRef		=models.CharField(max_length=18)
	commodityName		=models.CharField(max_length=100)
	commodityType		=models.CharField(max_length=9)
	def __unicode__(self):
		return self.commodityRef +' - ' + self.commodityName
	
class CommodityAdmin(admin.ModelAdmin):
	list_display = ('commodityRef', 'commodityName', 'commodityType')



class Waybill(models.Model):
	transaction_type_choice=(
			(u'INT', u'WFP Internal'),
#			(u'DIS', u'Distribution'),
#			(u'LON', u'Loan'),
#			(u'DSP', u'Disposal'),
#			(u'PUR', u'Purchase'),
#			(u'SHU',u'Shunting'),
#			(u'COS',u'Costal Transshipment'),
			(u'DEL',u'Delivery'),
#			(u'SWA',u'Swap'),
#			(u'REP',u'Repayment'),
#			(u'SAL',u'Sale'),
#			(u'ADR',u'Air drop'),
#			(u'INL',u'Inland Shipment')
		)
	transport_type=(
#			(u'R',u'Rail'),
			(u'T',u'Road'),
#			(u'A',u'Air'),
#			(u'I',u'Inland Waterways'),
#			(u'C',u'Costal Waterways'),
#			(u'M',u'Multi-mode'),
#			(u'O',u'Other Please Specify')
		)
	#general
	ltiNumber				=models.CharField(max_length=20)
	waybillNumber			=models.CharField(max_length=20)
	dateOfLoading			=models.DateField(null=True, blank=True)
	dateOfDispatch			=models.DateField(null=True, blank=True)
	transactionType			=models.CharField(max_length=10,choices=transaction_type_choice)
	transportType			=models.CharField(max_length=10,choices=transport_type)
	#Dispatcher
	dispatchRemarks			=models.TextField(blank=True,null=True)
	dispatcherName			=models.TextField(blank=True)
	dispatcherTitle			=models.TextField(blank=True)
	dispatcherSigned		=models.BooleanField(blank=True)
	#Transporter
	transportContractor			=models.TextField(blank=True)
	transportSubContractor		=models.TextField(blank=True)
	transportDriverName			=models.TextField(blank=True)
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
	containerOneSealNumber	=models.CharField(max_length=40,blank=True)
	containerTwoSealNumber	=models.CharField(max_length=40,blank=True)
	containerOneRemarksDispatch	=models.CharField(max_length=40,blank=True)
	containerTwoRemarksDispatch	=models.CharField(max_length=40,blank=True)
	containerOneRemarksReciept	=models.CharField(max_length=40,blank=True)
	containerTwoRemarksReciept	=models.CharField(max_length=40,blank=True)
	


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
		    SELECT DISTINCT ORIGIN_LOCATION_CODE,ORIGIN_LOC_NAME,ORIGIN_WH_NAME,ORIGIN_WH_CODE
		    FROM epic_lti
		    """)
		wh = cursor.fetchall()
		return wh
		
	def ltiCodes(self):
		cursor = connection.cursor()
		cursor.execute("""
		    SELECT DISTINCT CODE,ORIGIN_LOCATION_CODE,ORIGIN_LOC_NAME,ORIGIN_WH_NAME
		    FROM epic_lti order by LTI_ID
		    """)
		lti_code = cursor.fetchall()
		return lti_code
		
	def ltiCodesByWH(self,wh):
		cursor = connection.cursor()
		cursor.execute('SELECT DISTINCT CODE FROM epic_lti  WHERE ORIGIN_WH_CODE = %s order by LTI_ID',[wh])
		lti_code = cursor.fetchall()
		return lti_code
	
	def si_for_lti(self,lti_code):
		cursor = connection.cursor()
		cursor.execute("SELECT DISTINCT SI_CODE FROM epic_lti where CODE = %s",[lti_code])
		si_list = cursor.fetchall()
		return si_list
	
	

class ltioriginal(models.Model):
	LTI_PK				=models.CharField(max_length=50, primary_key=True)
	LTI_ID				=models.CharField(max_length=40)
	CODE            	=models.CharField(max_length=40)
	LTI_DATE			=models.DateField()
	EXPIRY_DATE			=models.DateField(blank=True,null=True)
	TRANSPORT_CODE		=models.CharField(max_length=4)
	TRANSPORT_OUC		=models.CharField(max_length=13)
	TRANSPORT_NAME		=models.CharField(max_length=30)
	ORIGIN_TYPE			=models.CharField(max_length=1)
	ORIGINTYPE_DESC     =models.CharField(max_length=12,blank=True)
	ORIGIN_LOCATION_CODE=models.CharField(max_length=10)
	ORIGIN_LOC_NAME		=models.CharField(max_length=30)
	ORIGIN_WH_CODE		=models.CharField(max_length=13,blank=True)
	ORIGIN_WH_NAME		=models.CharField(max_length=50,blank=True)
	DESTINATION_LOCATION_CODE	=models.CharField(max_length=10)
	DESTINATION_LOC_NAME=models.CharField(max_length=30)
	CONSEGNEE_CODE		=models.CharField(max_length=12)
	CONSEGNEE_NAME		=models.CharField(max_length=80)
	REQUESTED_DISPATCH_DATE		=models.DateField(blank=True,null=True)
	PROJECT_WBS_ELEMENT	=models.CharField(max_length=24,blank=True)
	SI_RECORD_ID		=models.CharField(max_length=25,blank=True)
	SI_CODE				=models.CharField(max_length=8)
	COMM_CATEGORY_CODE	=models.CharField(max_length=9)
	COMMODITY_CODE		=models.CharField(max_length=18)
	CMMNAME				=models.CharField(max_length=100,blank=True)
	QUANTITY_NET		=models.DecimalField(max_digits=11, decimal_places=3)
	QUANTITY_GROSS		=models.DecimalField(max_digits=11, decimal_places=3)
	NUMBER_OF_UNITS		=models.DecimalField(max_digits=7, decimal_places=0)
	UNIT_WEIGHT_NET		=models.DecimalField(max_digits=8, decimal_places=3,blank=True,null=True)
	UNIT_WEIGHT_GROSS	=models.DecimalField(max_digits=8, decimal_places=3,blank=True,null=True)
	
	objects = ltioriginalManager()
	class Meta:
		db_table = u'epic_lti'
		

	def  __unicode__(self):
		resting= ''
		#resting =  str(restant_si_item(self.LTI_ID,self.CMMNAME))
		return self.SI_CODE + ' ' + self.CMMNAME + ' ' + str(self.NUMBER_OF_UNITS)
	def mydesc(self):
		return self.CODE

####


### People Table

class EpicPerson(models.Model):
    person_pk 				= models.CharField(max_length=20, blank=True, primary_key=True)
    org_unit_code 			= models.CharField(max_length=13)
    code 					= models.CharField(max_length=7)
    type_of_document 		= models.CharField(max_length=2, blank=True)
    organization_id 		= models.CharField(max_length=12)
    last_name 				= models.CharField(max_length=30)
    first_name 				= models.CharField(max_length=25)
    title 					= models.CharField(max_length=50, blank=True)
    document_number 		= models.CharField(max_length=25, blank=True)
    e_mail_address 			= models.CharField(max_length=100, blank=True)
    mobile_phone_number 	= models.CharField(max_length=20, blank=True)
    official_tel_number 	= models.CharField(max_length=20, blank=True)
    fax_number 				= models.CharField(max_length=20, blank=True)
    effective_date 			= models.DateField(null=True, blank=True)
    expiry_date 			= models.DateField(null=True, blank=True)
    location_code 			= models.CharField(max_length=10)
    class Meta:
        db_table = u'epic_persons'
    def  __unicode__(self):
    	return self.last_name + ', ' + self.first_name
    	
class EpicPersonsAdmin(admin.ModelAdmin):
	list_display = ('last_name','first_name','title' , 'location_code')
	list_filter = ( 'location_code','organization_id')


class EpicStock(models.Model):
    wh_pk = models.CharField(max_length=90, blank=True, primary_key=True)
    wh_regional = models.CharField(max_length=4, blank=True)
    wh_country = models.CharField(max_length=15)
    wh_location = models.CharField(max_length=30)
    wh_code = models.CharField(max_length=13)
    wh_name = models.CharField(max_length=50, blank=True)
    project_wbs_element = models.CharField(max_length=24, blank=True)
    si_record_id = models.CharField(max_length=25)
    si_code = models.CharField(max_length=8)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    cmmname = models.CharField(max_length=100, blank=True)
    package_code = models.CharField(max_length=17)
    packagename = models.CharField(max_length=50, blank=True)
    qualitycode = models.CharField(max_length=1)
    qualitydescr = models.CharField(max_length=11, blank=True)
    quantity_net = models.DecimalField(null=True, max_digits=12, decimal_places=3, blank=True)
    quantity_gross = models.DecimalField(null=True, max_digits=12, decimal_places=3, blank=True)
    number_of_units = models.IntegerField()
    allocation_code = models.CharField(max_length=10)
    reference_number= models.CharField(max_length=50)
    class Meta:
        db_table = u'epic_stock'

### Stock ??



class LoadingDetail(models.Model):
	wbNumber				=models.ForeignKey(Waybill)
	siNo					=models.ForeignKey(ltioriginal)
	numberUnitsLoaded		=models.IntegerField(blank=True,null=True)
	numberUnitsGood			=models.IntegerField(blank=True,null=True)
	numberUnitsLost			=models.IntegerField(blank=True,null=True)
	numberUnitsDamaged		=models.IntegerField(blank=True,null=True)
	unitsLostReason			=models.TextField(blank=True)
	unitsDamagedReason		=models.TextField(blank=True)
	
	
	def calcTotalNet(self):
		totalNet =( self.numberUnitsLoaded + self.siNo.UNIT_WEIGHT_NET)/1000
		return totalNet
	def calcTotalGross(self):
		totalGross =( self.numberUnitsLoaded + self.siNo.UNIT_WEIGHT_GROSS)/1000
		return totalGross
		
	
	def  __unicode__(self):
		return self.wbNumber.mydesc() +' - '+ self.siNo.mydesc()


class DispachPoint(models.Model):
	ORIGIN_LOC_NAME			=models.CharField(max_length=11, blank=True)
	ORIGIN_LOCATION_CODE	=models.CharField(max_length=11, blank=True)
	ORIGIN_WH_CODE			=models.CharField(max_length=11, blank=True)
	ORIGIN_WH_NAME			=models.CharField(max_length=11, blank=True)
	
	def  __unicode__(self):
		return self.ORIGIN_WH_CODE
	
class ETSRole(models.Model):
	roleName				=models.CharField(max_length=50, blank=True)
	isCompas				=models.BooleanField()
	isDispatcher			=models.BooleanField()
	isReciever				=models.BooleanField()
	
	def __unicode__(self):
		return self.roleName
	
class UserProfile(models.Model):
	user					=models.OneToOneField(User, primary_key=True)
	warehouses				=models.ManyToManyField(DispachPoint)
	isCompasUser			=models.BooleanField()
	isDispatcher			=models.BooleanField()
	isReciever				=models.BooleanField()
	compasUser				=models.OneToOneField(EpicPerson)
	
	def __unicode__(self):
		return self.user.get_full_name()
		
class UserProfileAdmin(admin.ModelAdmin):
	list_display=('user','warehouses')
	

class SIWithRestant:
	SINumber = ''
	StartAmount = 0
	CurrentAmount = 0
	CommodityName = ''
	def __init__(self,SINumber,StartAmount,CommodityName):
		self.SINumber = SINumber
		self.StartAmount = StartAmount
		self.CurrentAmount = StartAmount
		self.CommodityName = CommodityName
	
	def reduceCurrent(self,reduce):
		self.CurrentAmount = int(self.CurrentAmount) - reduce
	def getCurrentAmount(self):
		return self.CurrentAmount
	def getStartAmount(self):
		return StartAmount

	
class LoadingDetailInline(admin.TabularInline):
	model = LoadingDetail

class WaybillAdmin(admin.ModelAdmin):
	list_display=('waybillNumber','ltiNumber')
	inlines = [LoadingDetailInline]

class LoadingDetailAdmin(admin.ModelAdmin):
	list_display=('waybillNumber','siNo')

class ltioriginalAdmin(admin.ModelAdmin):
	list_display=('CODE','SI_CODE')



admin.site.register(Commodity,CommodityAdmin)
admin.site.register(Waybill,WaybillAdmin)
admin.site.register(LoadingDetail)
admin.site.register(ltioriginal,ltioriginalAdmin)
admin.site.register(UserProfile)
admin.site.register(ETSRole)
admin.site.register(DispachPoint)
admin.site.register(EpicPerson,EpicPersonsAdmin)