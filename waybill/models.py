from django.db import models, connection
from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
import datetime
from django.template.defaultfilters import stringfilter
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog


# Create your models here.

class places(models.Model):
		ORG_CODE 			=models.CharField(max_length=7, primary_key=True)
		NAME				=models.CharField(max_length=100)
		GEO_POINT_CODE 		=models.CharField(max_length=4)
		GEO_NAME			=models.CharField(max_length=100)
		COUNTRY_CODE		=models.CharField(max_length=3)
		REPORTING_CODE 		=models.CharField(max_length=7)
		ORGANIZATION_ID 	=models.CharField(max_length=20)
		def __unicode__(self):
				return self.NAME

		class Meta:
				db_table = u'epic_geo'

class Waybill(models.Model):
		transaction_type_choice=(
						(u'WIT', u'WFP Internal'),
#						(u'DIS', u'Distribution'),
#						(u'LON', u'Loan'),
#						(u'DSP', u'Disposal'),
#						(u'PUR', u'Purchase'),
#						(u'SHU',u'Shunting'),
#						(u'COS',u'Costal Transshipment'),
						(u'DEL',u'Delivery'),
#						(u'SWA',u'Swap'),
#						(u'REP',u'Repayment'),
#						(u'SAL',u'Sale'),
#						(u'ADR',u'Air drop'),
#						(u'INL',u'Inland Shipment')
				)
		transport_type=(
#						(u'01',u'Rail'),
						(u'02',u'Road'),
#						(u'04',u'Air'),
#						(u'I',u'Inland Waterways'),
#						(u'C',u'Costal Waterways'),
#						(u'07',u'Multi-mode'),
#						(u'O',u'Other Please Specify')
				)
		
				
		#general
		ltiNumber						=models.CharField(max_length=20)
		waybillNumber					=models.CharField(max_length=20)
		dateOfLoading					=models.DateField(null=True, blank=True)
		dateOfDispatch					=models.DateField(null=True, blank=True)
		transactionType					=models.CharField(max_length=10,choices=transaction_type_choice)
		transportType					=models.CharField(max_length=10,choices=transport_type)
		#Dispatcher
		dispatchRemarks					=models.CharField(max_length=200)
		dispatcherName					=models.TextField(blank=True,null=True)
		dispatcherTitle					=models.TextField(blank=True)
		dispatcherSigned				=models.BooleanField(blank=True)
		#Transporter
		transportContractor				=models.TextField(blank=True)
		transportSubContractor			=models.TextField(blank=True)
		transportDriverName				=models.TextField(blank=True)
		transportDriverLicenceID		=models.TextField(blank=True)
		transportVehicleRegistration	=models.TextField(blank=True)
		transportTrailerRegistration	=models.TextField(blank=True)
		transportDispachSigned			=models.BooleanField(blank=True)
		transportDispachSignedTimestamp	=models.DateTimeField(null=True, blank=True)
		transportDeliverySigned			=models.BooleanField(blank=True)
		transportDeliverySignedTimestamp=models.DateTimeField(null=True, blank=True)

		#Container		
		containerOneNumber				=models.CharField(max_length=40,blank=True)
		containerTwoNumber				=models.CharField(max_length=40,blank=True)
		containerOneSealNumber			=models.CharField(max_length=40,blank=True)
		containerTwoSealNumber			=models.CharField(max_length=40,blank=True)
		containerOneRemarksDispatch		=models.CharField(max_length=40,blank=True)
		containerTwoRemarksDispatch		=models.CharField(max_length=40,blank=True)
		containerOneRemarksReciept		=models.CharField(max_length=40,blank=True)
		containerTwoRemarksReciept		=models.CharField(max_length=40,blank=True)

		#Reciver
		recipientLocation				=models.CharField(max_length=100,blank=True)
		recipientConsingee				=models.CharField(max_length=100,blank=True)
		recipientName					=models.CharField(max_length=100,blank=True)
		recipientTitle					=models.CharField(max_length=100,blank=True)
		recipientArrivalDate			=models.DateField(null=True, blank=True)
		recipientStartDischargeDate		=models.DateField(null=True, blank=True)
		recipientEndDischargeDate		=models.DateField(null=True, blank=True)
		recipientDistance				=models.IntegerField(blank=True,null=True)
		recipientRemarks				=models.TextField(blank=True)
		recipientSigned					=models.BooleanField(blank=True)
		recipientSignedTimestamp		=models.DateTimeField(null=True, blank=True)
		destinationWarehouse 			=models.ForeignKey(places,blank=True)

		#Extra Fields
		waybillValidated				=models.BooleanField()
		waybillReceiptValidated 		=models.BooleanField()
		waybillSentToCompas 			=models.BooleanField()
		waybillRecSentToCompas 			=models.BooleanField()
		waybillProcessedForPayment		=models.BooleanField()
		invalidated						=models.BooleanField()
		audit_log = AuditLog()
		
		def  __unicode__(self):
				return self.waybillNumber
		def mydesc(self):
				return self.waybillNumber
		def errors(self):
			return loggerCompas.objects.get(wb=self)

#### Compas Tables Imported

"""
Models based on compas Views & Tables
"""
class ltioriginalManager(models.Manager):
 		"""
 		Manager for the LTIOriginal Model
 		these functions are related to the whole model/table not individual rows
 		some should be replaced using filter objects.view()
 		"""
				
		def ltiCodesByWH(self,wh):
				cursor = connection.cursor()
				cursor.execute('SELECT DISTINCT CODE,DESTINATION_LOC_NAME,CONSEGNEE_NAME,REQUESTED_DISPATCH_DATE FROM epic_lti  WHERE ORIGIN_WH_CODE = %s  and  SI_RECORD_ID in  (select si_record_id from epic_stock)  and CONSEGNEE_NAME in (select CONSEGNEE_NAME from waybill_receptionpoint )',[wh])
				lti_code = cursor.fetchall()
				#lti2_codes = ltioriginal.objects.filter(ORIGIN_WH_CODE=wh).values('CODE','DESTINATION_LOC_NAME','CONSEGNEE_NAME','REQUESTED_DISPATCH_DATE').extra(where=['SI_RECORD_ID in  (select si_record_id from epic_stock)','CONSEGNEE_NAME in (select CONSEGNEE_NAME from waybill_receptionpoint )']).distinct()
				return lti_code
		
		def ltiCodesAll(self):
				cursor = connection.cursor()
				cursor.execute('SELECT DISTINCT CODE,DESTINATION_LOC_NAME,CONSEGNEE_NAME,REQUESTED_DISPATCH_DATE,ORIGIN_LOC_NAME FROM epic_lti  WHERE SI_RECORD_ID in  (select si_record_id from epic_stock)  and CONSEGNEE_NAME in (select CONSEGNEE_NAME from waybill_receptionpoint )')
				lti_code = cursor.fetchall()
				#lti2_codes = ltioriginal.objects.filter(ORIGIN_WH_CODE=wh).values('CODE','DESTINATION_LOC_NAME','CONSEGNEE_NAME','REQUESTED_DISPATCH_DATE').extra(where=['SI_RECORD_ID in  (select si_record_id from epic_stock)','CONSEGNEE_NAME in (select CONSEGNEE_NAME from waybill_receptionpoint )']).distinct()
				return lti_code
		
		def si_for_lti(self,lti_code):
				cursor = connection.cursor()
				cursor.execute("SELECT DISTINCT SI_CODE FROM epic_lti where CODE = %s",[lti_code])
				si_list = cursor.fetchall()
				return si_list
				
class ltioriginal(models.Model):
		LTI_PK						=models.CharField(max_length=50, primary_key=True)
		LTI_ID						=models.CharField(max_length=40)
		CODE            			=models.CharField(max_length=40)
		LTI_DATE					=models.DateField()
		EXPIRY_DATE					=models.DateField(blank=True,null=True)
		TRANSPORT_CODE				=models.CharField(max_length=4)
		TRANSPORT_OUC				=models.CharField(max_length=13)
		TRANSPORT_NAME				=models.CharField(max_length=30)
		ORIGIN_TYPE					=models.CharField(max_length=1)
		ORIGINTYPE_DESC				=models.CharField(max_length=12,blank=True)
		ORIGIN_LOCATION_CODE		=models.CharField(max_length=10)
		ORIGIN_LOC_NAME				=models.CharField(max_length=30)
		ORIGIN_WH_CODE				=models.CharField(max_length=13,blank=True)
		ORIGIN_WH_NAME				=models.CharField(max_length=50,blank=True)
		DESTINATION_LOCATION_CODE	=models.CharField(max_length=10)
		DESTINATION_LOC_NAME		=models.CharField(max_length=30)
		CONSEGNEE_CODE				=models.CharField(max_length=12)
		CONSEGNEE_NAME				=models.CharField(max_length=80)
		REQUESTED_DISPATCH_DATE		=models.DateField(blank=True,null=True)
		PROJECT_WBS_ELEMENT			=models.CharField(max_length=24,blank=True)
		SI_RECORD_ID				=models.CharField(max_length=25,blank=True)
		SI_CODE						=models.CharField(max_length=8)
		COMM_CATEGORY_CODE			=models.CharField(max_length=9)
		COMMODITY_CODE				=models.CharField(max_length=18)
		CMMNAME						=models.CharField(max_length=100,blank=True)
		QUANTITY_NET				=models.DecimalField(max_digits=11, decimal_places=3)
		QUANTITY_GROSS				=models.DecimalField(max_digits=11, decimal_places=3)
		NUMBER_OF_UNITS				=models.DecimalField(max_digits=7, decimal_places=0)
		UNIT_WEIGHT_NET				=models.DecimalField(max_digits=8, decimal_places=3,blank=True,null=True)
		UNIT_WEIGHT_GROSS			=models.DecimalField(max_digits=8, decimal_places=3,blank=True,null=True)
		
		objects = ltioriginalManager()
		
		
		class Meta:
				db_table = u'epic_lti'
				
		def  __unicode__(self):
				marker = ''
				
				#if self.LTI_PK in removedLtis.objects.list():
				#	marker = 'Void '
				return self.valid() + self.coi_code() + '  ' + self.CMMNAME + '  %.0f'  %  self.restant2() 
		def mydesc(self):
				return self.CODE
		def commodity(self):
				return self.CMMNAME 
		def restant(self):
				return self.sitracker.number_units_left
		def valid(self):
			if removedLtis.objects.filter(lti = self.LTI_PK):
				return "Void "
			else:
				return ''
		def restant2(self):
				lines = LoadingDetail.objects.filter(siNo=self)
				used = 0
#				print 'xxx'
				for line in lines:
					used +=  line.numberUnitsLoaded
#					print  line.numberUnitsLoaded
#					print line
#					print 'Used:' + str(used)
				return self.NUMBER_OF_UNITS - used
		def reducesi(self,units):
				self.sitracker.updateUnits(units)
				return self.restant()
		def restoresi(self,units):
				self.sitracker.updateUnitsRestore(units)
				return self.restant()
		def coi_code(self):
				try:
						cursor = connection.cursor()
						cursor.execute("SELECT origin_id from epic_stock where  (WH_CODE=%s  and SI_CODE=%s and COMMODITY_CODE=%s )",[self.ORIGIN_WH_CODE,self.SI_CODE,self.COMMODITY_CODE])
						stock = cursor.fetchall()
						item = stock[0]
						return str(item[0][7:])
						
				except:
					try:
						cursor = connection.cursor()
						cursor.execute("SELECT origin_id from epic_stock where  ( SI_CODE=%s and COMM_CATEGORY_CODE=%s )",[self.SI_CODE,self.COMM_CATEGORY_CODE])
						stock = cursor.fetchall()
						item = stock[0]
						return str(item[0][7:])
					except:				
						try:
							cursor = connection.cursor()
							cursor.execute("SELECT origin_id from epic_stock where  (WH_CODE=%s  and SI_CODE=%s and COMM_CATEGORY_CODE=%s )",[self.ORIGIN_WH_CODE,self.SI_CODE,self.COMM_CATEGORY_CODE])
							stock = cursor.fetchall()
							item = stock[0]
							return str(item[0][7:])
						except:				
							return 'No Stock '
		def remove_lti(self):
			this_lti = removedLtis()
			this_lti.lti = self
			this_lti.save()
			
class removedLtisManager(models.Manager):
		def list(self):
			listExl =[]
			listOfExcluded = removedLtis.objects.all()
			for exl in listOfExcluded:
				listExl += [exl.lti.LTI_PK]
			return listExl
## helper table for nolonger existing lti items
class removedLtis(models.Model):
		lti = models.ForeignKey(ltioriginal)
		
		objects = removedLtisManager()
		class Meta:
				db_table = u'waybill_removed_ltis'
	

class EpicPerson(models.Model):
		person_pk 					= models.CharField(max_length=20, blank=True, primary_key=True)
		org_unit_code 				= models.CharField(max_length=13)
		code 						= models.CharField(max_length=7)
		type_of_document 			= models.CharField(max_length=2, blank=True)
		organization_id 			= models.CharField(max_length=12)
		last_name 					= models.CharField(max_length=30)
		first_name 					= models.CharField(max_length=25)
		title 						= models.CharField(max_length=50, blank=True)
		document_number 			= models.CharField(max_length=25, blank=True)
		e_mail_address 				= models.CharField(max_length=100, blank=True)
		mobile_phone_number 		= models.CharField(max_length=20, blank=True)
		official_tel_number 		= models.CharField(max_length=20, blank=True)
		fax_number 					= models.CharField(max_length=20, blank=True)
		effective_date 				= models.DateField(null=True, blank=True)
		expiry_date 				= models.DateField(null=True, blank=True)
		location_code 				= models.CharField(max_length=10)

		class Meta:
				db_table = u'epic_persons'
		def  __unicode__(self):
				return self.last_name + ', ' + self.first_name
				
class EpicPersonsAdmin(admin.ModelAdmin):
		list_display = ('last_name','first_name','title' , 'location_code')
		list_filter = ( 'location_code','organization_id')

class EpicStock(models.Model):
		wh_pk 				= models.CharField(max_length=90, blank=True, primary_key=True)
		wh_regional 		= models.CharField(max_length=4, blank=True)
		wh_country 			= models.CharField(max_length=15)
		wh_location 		= models.CharField(max_length=30)
		wh_code 			= models.CharField(max_length=13)
		wh_name 			= models.CharField(max_length=50, blank=True)
		project_wbs_element = models.CharField(max_length=24, blank=True)
		si_record_id 		= models.CharField(max_length=25)
		si_code 			= models.CharField(max_length=8)
		origin_id 			= models.CharField(max_length=23)
		comm_category_code 	= models.CharField(max_length=9)
		commodity_code 		= models.CharField(max_length=18)
		cmmname 			= models.CharField(max_length=100, blank=True)
		package_code 		= models.CharField(max_length=17)
		packagename 		= models.CharField(max_length=50, blank=True)
		qualitycode 		= models.CharField(max_length=1)
		qualitydescr 		= models.CharField(max_length=11, blank=True)
		quantity_net 		= models.DecimalField(null=True, max_digits=12, decimal_places=3, blank=True)
		quantity_gross 		= models.DecimalField(null=True, max_digits=12, decimal_places=3, blank=True)
		number_of_units 	= models.IntegerField()
		allocation_code 	= models.CharField(max_length=10)
		reference_number	= models.CharField(max_length=50)

		class Meta:
				db_table = u'epic_stock'
		
		def packagingDescrShort(self):
			pck= PackagingDescriptonShort.objects.get(pk=self.package_code)
			#print pck
			return pck.packageShortName
			
class EpicLossReason(models.Model):
		REASON_CODE =models.CharField(max_length=5,primary_key=True)
		REASON =models.CharField(max_length=80)
		class Meta:
				db_table = u'epic_lossreason'
		def  __unicode__(self):
				return self.REASON		

class LossesDamagesReason(models.Model):
		compasRC = models.ForeignKey(EpicLossReason)
		compasCode= models.CharField(max_length=20)
		description  = models.CharField(max_length=20)
		
		def  __unicode__(self):
				return self.description

class LossesDamagesReasonAdmin(admin.ModelAdmin):
		list_display = ('compasCode','description','compasRC')
		list_filter = ('compasRC',) 
		
class LossesDamagesType(models.Model):
		description = models.CharField(max_length=20)
		
		def  __unicode__(self):
				return self.description

class LoadingDetail(models.Model):
		wbNumber					=models.ForeignKey(Waybill)
		siNo						=models.ForeignKey(ltioriginal)
		numberUnitsLoaded			=models.DecimalField(default=0, blank=True,null=True,max_digits=10, decimal_places=3)
		numberUnitsGood				=models.DecimalField(default=0,blank=True,null=True,max_digits=10, decimal_places=3)
		numberUnitsLost				=models.DecimalField(default=0,blank=True,null=True,max_digits=10, decimal_places=3)
		numberUnitsDamaged			=models.DecimalField(default=0,blank=True,null=True,max_digits=10, decimal_places=3)
		unitsLostReason				=models.ForeignKey(LossesDamagesReason,related_name='LD_LostReason',blank=True,null=True)
		unitsDamagedReason			=models.ForeignKey(LossesDamagesReason,related_name='LD_DamagedReason',blank=True,null=True)
		unitsDamagedType 			=models.ForeignKey(LossesDamagesType,related_name='LD_DamagedType',blank=True,null=True)
		unitsLostType 				=models.ForeignKey(LossesDamagesType,related_name='LD_LossType',blank=True,null=True)
		overloadedUnits				=models.BooleanField()
		loadingDetailSentToCompas 	=models.BooleanField()
		
		audit_log = AuditLog()
		
		
		def getStockItem(self):
			try:
				stockItem = EpicStock.objects.filter(si_code = self.siNo.SI_CODE).filter(commodity_code = self.siNo.COMMODITY_CODE)
				return stockItem[0]
			except:
				try:
					stockItem = EpicStock.objects.filter(si_code = self.siNo.SI_CODE).filter(comm_category_code = self.siNo.COMM_CATEGORY_CODE)
					return stockItem[0]
				except:
					return 'N/A'
		
		def calcTotalNet(self):
				totalNet =( self.numberUnitsLoaded * self.siNo.UNIT_WEIGHT_NET)/1000
				return totalNet
		def calcTotalGross(self):
				totalGross =( self.numberUnitsLoaded * self.siNo.UNIT_WEIGHT_GROSS)/1000
				return totalGross
				
		def calcNetRecievedGood(self):
				totalNet =( self.numberUnitsGood * self.siNo.UNIT_WEIGHT_NET)/1000
				return totalNet
		def calcGrossRecievedGood(self):
				totalGross =( self.numberUnitsGood * self.siNo.UNIT_WEIGHT_GROSS)/1000
				return totalGross

		def calcNetRecievedDamaged(self):
				totalNet =( self.numberUnitsDamaged * self.siNo.UNIT_WEIGHT_NET)/1000
				return totalNet
		def calcGrossRecievedDamaged(self):
				totalGross =( self.numberUnitsDamaged * self.siNo.UNIT_WEIGHT_GROSS)/1000
				return totalGross

		def calcNetRecievedLost(self):
				totalNet =( self.numberUnitsLost * self.siNo.UNIT_WEIGHT_NET)/1000
				return totalNet
		def calcGrossRecievedLost(self):
				totalGross =( self.numberUnitsLost * self.siNo.UNIT_WEIGHT_GROSS)/1000
				return totalGross
		def calcTotalReceivedUnits(self):
				total = self.numberUnitsGood + self.numberUnitsDamaged 
				return total
		def calcTotalReceivedNet(self):
				total = self.calcNetRecievedGood() + self.calcNetRecievedDamaged() 
				return total
		
		def  __unicode__(self):
				return self.wbNumber.mydesc() +' - '+ self.siNo.mydesc()  +' - '+ self.siNo.LTI_PK

class DispatchPoint(models.Model):
		ORIGIN_LOC_NAME						=models.CharField(max_length=20, blank=True)
		ORIGIN_LOCATION_CODE				=models.CharField(max_length=20, blank=True)
		ORIGIN_WH_CODE						=models.CharField(max_length=20, blank=True)
		ORIGIN_WH_NAME						=models.CharField(max_length=30, blank=True)
		DESC_NAME							=models.CharField(max_length=20, blank=True,null=True)
		
		def  __unicode__(self):
				return self.ORIGIN_WH_CODE + ' - ' + self.ORIGIN_LOC_NAME
		
class ReceptionPoint(models.Model):
		LOC_NAME				=models.CharField(max_length=20, blank=True)
		LOCATION_CODE			=models.CharField(max_length=20, blank=True)
		CONSEGNEE_CODE			=models.CharField(max_length=20, blank=True)
		CONSEGNEE_NAME			=models.CharField(max_length=80, blank=True)
		#DESC_NAME				=models.CharField(max_length=80, blank=True)
		def  __unicode__(self):
				return self.LOC_NAME + ' ' + self.CONSEGNEE_CODE + ' - ' + self.CONSEGNEE_NAME

class UserProfile(models.Model):
		user				=models.OneToOneField(User, primary_key=True)
		warehouses			=models.ForeignKey(DispatchPoint, blank=True,null=True)
		receptionPoints		=models.ForeignKey(ReceptionPoint, blank=True,null=True)
		isCompasUser		=models.BooleanField()
		isDispatcher		=models.BooleanField()
		isReciever			=models.BooleanField()
		compasUser			=models.ForeignKey(EpicPerson, blank=True,null=True)
		superUser			=models.BooleanField()
		readerUser			=models.BooleanField()
		audit_log = AuditLog()		
		def __unicode__(self):
				return "%s's profile" % self.user 

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
				
class UserProfileAdmin(admin.ModelAdmin):
		list_display=('user','warehouses')
		
class SiTracker(models.Model):
		LTI 				= models.OneToOneField(ltioriginal,primary_key=True)
		number_units_left 	= models.DecimalField(decimal_places=3,max_digits=10)
		number_units_start 	= models.DecimalField(decimal_places=3,max_digits=10)
				
		def updateUnits(self,ammount):
				self.number_units_left -=ammount
				self.save()
		def updateUnitsRestore(self,ammount):
				self.number_units_left +=ammount
				self.save()
		def  __unicode__(self):
				return self.number_units_left

class PackagingDescriptonShort(models.Model):
		packageCode 		= models.CharField(primary_key=True,max_length=5)
		packageShortName 	= models.CharField(max_length=10)
		def  __unicode__(self):
				return self.packageCode+' - '+ self.packageShortName
				
class PackagingDescriptonShortAdmin(admin.ModelAdmin):
		list_display=('packageCode','packageShortName')
		list_filter = ('packageCode','packageShortName') 
		
class loggerCompas(models.Model):
 	timestamp		= models.DateTimeField(null=True, blank=True)
 	user			= models.ForeignKey(User)
 	action			= models.CharField(max_length=50, blank=True)
 	errorRec		= models.CharField(max_length=200, blank=True)
 	errorDisp		= models.CharField(max_length=200, blank=True)
 	wb				= models.ForeignKey(Waybill, blank=True,primary_key=True)
 	lti				= models.CharField(max_length=50, blank=True)
 	data_in			= models.CharField(max_length=5000, blank=True)
 	data_out		= models.CharField(max_length=5000, blank=True)


	
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
		
class LoadingDetailAdmin(admin.ModelAdmin):
		list_display=('waybillNumber','siNo')

admin.site.register(UserProfile)
admin.site.register(DispatchPoint)
admin.site.register(ReceptionPoint)
admin.site.register(EpicPerson,EpicPersonsAdmin)
admin.site.register(LossesDamagesReason,LossesDamagesReasonAdmin)
admin.site.register(LossesDamagesType)
admin.site.register(PackagingDescriptonShort,PackagingDescriptonShortAdmin)
admin.site.register(EpicLossReason)