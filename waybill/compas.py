import cx_Oracle
from ets.waybill.models import *
from ets.waybill.forms import *
from ets.waybill.views import *
from django.db import models
from django.db import connections
from django.conf import settings
import datetime

class compas_write:
	ErrorMessages = ''
	ErrorCodes = ''

	def __init__(self):
		self.__db = cx_Oracle.Connection(settings.DATABASES['compas']['USER']+'/'+settings.DATABASES['compas']['PASSWORD']+'@//'+ settings.DATABASES['compas']['HOST'] +':1521/'+settings.COMPAS_STATION)
		self.__cursor = self.__db.cursor()

	def __del__(self):
   		self.__cursor.close()
		self.__db.close()
		
	def test_cps(self):
		db = self.__db
		cursor = self.__cursor
		
		cursor.arraysize = 50
		cursor.execute("select * from Epic_Geo")

		for column_1, column_2, column_3,col4,col5,col6,col7 in cursor.fetchall():
			print "Values from DB:", column_1, column_2, column_3



	def write_receipt_waybill_compas(self,waybill_id):
		#db = cx_Oracle.Connection(settings.DATABASES['compas']['USER']+'/'+settings.DATABASES['compas']['PASSWORD']+'@//'+ settings.DATABASES['compas']['HOST'] +':1521/'+settings.COMPAS_STATION)
		#cursor =  db.cursor()#connections['compas'].cursor()		
		db = self.__db
		cursor = self.__cursor
		self.ErrorMessages = ''
		self.ErrorCodes = ''
		the_waybill = Waybill.objects.get(id=waybill_id)
		lineItems = the_waybill.loadingdetail_set.select_related()
		WB_CODE = the_waybill.waybillNumber
		receiverPerson  = EpicPerson.objects.get(person_pk = the_waybill.recipientName)
		recPersonOUC = receiverPerson.org_unit_code
		recPersonCode = receiverPerson.code
		arrival_date = str(the_waybill.recipientArrivalDate.strftime("%Y%m%d"))
		all_ok = True
		## check if containers = 2 & lines = 2
		twoCont = False
		if lineItems.count() == 2:
			if len(the_waybill.containerTwoNumber) > 0:
				twoCont = True
		codeLetter = 'A'
		db.begin()
		loopNumber = 0
		for lineItem in lineItems:
			loopNumber = loopNumber+1
			CURR_CODE=str(datetime.datetime.now().strftime('%y') +WB_CODE)
			if twoCont:
				CURR_CODE = str(datetime.datetime.now().strftime('%y') + codeLetter + WB_CODE)
				codeLetter = 'B'
			
			goodUnits = str(lineItem.numberUnitsGood)
			if lineItem.numberUnitsDamaged > 0:
				damadgedUnits =str(lineItem.numberUnitsDamaged)
				damadgedReason = str(lineItem.unitsDamagedReason.compasCode)
			else:
				damadgedReason = ''
				damadgedUnits = ''
			if lineItem.numberUnitsLost:
				lostUnits =str(lineItem.numberUnitsLost)
				lossReason = str(lineItem.unitsLostReason.compasCode)
			else:
				lossReason = ''
				lostUnits = ''

			COI_CODE = str(lineItem.siNo.coi_code())			
			TheStockItems = EpicStock.objects.filter(origin_id__contains=COI_CODE)
			Full_coi= TheStockItems[0].origin_id

			COMM_CATEGORY_CODE = lineItem.siNo.COMM_CATEGORY_CODE
			COMM_CODE = lineItem.siNo.COMMODITY_CODE
			#get stock
			PCKKCODE = TheStockItems[0].package_code
			ALLCODE = TheStockItems[0].allocation_code
			QUALITY = TheStockItems[0].qualitycode #'G'
			
			Response_Message = cursor.var(cx_Oracle.STRING)
			Response_Message.setvalue(0,' '*200)
			Response_Code = cursor.var(cx_Oracle.STRING)
			Response_Code.setvalue(0,' ')
			trans = [Response_Message,
				Response_Code,
				CURR_CODE,
				recPersonOUC,
				recPersonCode,
				arrival_date,
				goodUnits,
				damadgedReason,
				damadgedUnits,
				lossReason,
				lostUnits,
				Full_coi,
				COMM_CATEGORY_CODE,
				COMM_CODE,
				PCKKCODE,
				ALLCODE,
				QUALITY]

			cursor.callproc('write_waybill.receipt',(
				Response_Message,
				Response_Code,
				CURR_CODE,
				recPersonOUC,
				recPersonCode,
				arrival_date,
				goodUnits,
				damadgedReason,
				damadgedUnits,
				lossReason,
				lostUnits,
				Full_coi,
				COMM_CATEGORY_CODE,
				COMM_CODE,
				PCKKCODE,
				ALLCODE,
				QUALITY
				))
				
			if(	Response_Code.getvalue() == 'S'):
				pass
			else:
				all_ok =False
				self.ErrorMessages +=str(loopNumber) + Full_coi+":"+Response_Message.getvalue() + " "
				self.ErrorCodes += str(loopNumber) + Full_coi+":"+ Response_Code.getvalue()+ " "
		
		print  Response_Message.getvalue()
		if not all_ok:
			db.rollback()
		else:
			db.commit()

			
		cursor.close()
		db.close()
		return all_ok

		cursor.close()

		
	def write_dispatch_waybill_compas(self,waybill_id):
		db = self.__db
		cursor = self.__cursor
		
		self.ErrorMessages = ''
		self.ErrorCodes = ''
		
		# gather wb info
		the_waybill = Waybill.objects.get(id=waybill_id)
		lineItems = the_waybill.loadingdetail_set.select_related()
		LTI= lineItems[0].siNo
		dispatch_person = EpicPerson.objects.get(person_pk = the_waybill.dispatcherName)
		# make dispatch remarks::::
		dispatch_remarks = the_waybill.dispatchRemarks
		CODE =  the_waybill.waybillNumber
		DOCUMENT_CODE = 'wb'
		DISPATCH_DATE=str(the_waybill.dateOfDispatch.strftime("%Y%m%d"))
		ORIGIN_TYPE=LTI.ORIGIN_TYPE
		ORIGIN_LOCATION_CODE=LTI.ORIGIN_LOCATION_CODE
		ORIGIN_CODE=LTI.ORIGIN_WH_CODE
		ORIGIN_DESCR=''
		DESTINATION_LOCATION_CODE=LTI.DESTINATION_LOCATION_CODE
		DESTINATION_CODE=str(the_waybill.destinationWarehouse.ORG_CODE)
		PRO_ACTIVITY_CODE=u""
		ACTIVITY_OUC=u""
		LNDARRM_CODE=u""
		LTI_ID=LTI.LTI_ID
		LOADING_DATE=str(the_waybill.dateOfLoading.strftime("%Y%m%d"))
		ORGANIZATION_ID=LTI.CONSEGNEE_CODE
		TRAN_TYPE_CODE=the_waybill.transactionType
		TRAN_TYPE_DESCR=the_waybill.transportVehicleRegistration
		MODETRANS_CODE=the_waybill.transportType
		COMMENTS=	dispatch_remarks
		PERSON_CODE=dispatch_person.code
		PERSON_OUC=dispatch_person.org_unit_code
		CERTIFING_TITLE=dispatch_person.title
		TRANS_CONTRACTOR_CODE=LTI.TRANSPORT_CODE
		SUPPLIER1_OUC=LTI.TRANSPORT_OUC
		DRIVER_NAME=the_waybill.transportDriverName
		LICENSE=the_waybill.transportDriverLicenceID
		VEHICLE_REGISTRATION=the_waybill.transportVehicleRegistration
		TRAILER_PLATE=the_waybill.transportTrailerRegistration
		CONTAINER_NUMBER=the_waybill.containerOneNumber			
		## For each lineItems
		all_ok = True
		## check if containers = 2 & lines = 2
		twoCont = False
		if lineItems.count() == 2:
			if len(the_waybill.containerTwoNumber) > 0:
				twoCont = True
		codeLetter = 'A'
		db.begin()
		loopNumber = 0
		for lineItem in lineItems:
			loopNumber = loopNumber+1
			CURR_CONTAINER_NUMBER=CONTAINER_NUMBER
			CURR_CODE=str(datetime.datetime.now().strftime('%y') +CODE)
			if twoCont:
				CURR_CODE = str(datetime.datetime.now().strftime('%y') + codeLetter + CODE)
				codeLetter = 'B'
				CONTAINER_NUMBER=str(the_waybill.containerTwoNumber)		
				
				
			COMM_CATEGORY_CODE = lineItem.siNo.COMM_CATEGORY_CODE
			COMM_CODE = lineItem.siNo.COMMODITY_CODE
			COI_CODE = str(lineItem.siNo.coi_code())			
			#get stock
			TheStockItems = EpicStock.objects.filter(origin_id__contains=COI_CODE)
			PCKKCODE = TheStockItems[0].package_code
			ALLCODE = TheStockItems[0].allocation_code
			QUALITY = TheStockItems[0].qualitycode #'G'
			UnitsLoaded = lineItem.numberUnitsLoaded
			UnitNet= lineItem.siNo.UNIT_WEIGHT_NET
			UnitGross = lineItem.siNo.UNIT_WEIGHT_GROSS
			
			NetTotal =(UnitNet * UnitsLoaded) / 1000
			strNetTotal = '%.3f' % NetTotal
			GrossTotal = (UnitGross * UnitsLoaded) / 1000
			strGrossTotal = '%.3f' % GrossTotal

			Response_Message = cursor.var(cx_Oracle.STRING)
			Response_Message.setvalue(0,' '*200)
			Response_Code = cursor.var(cx_Oracle.STRING)
			Response_Code.setvalue(0,' '*2)
			Full_coi= TheStockItems[0].origin_id
			empty = ''

 			trans = [CURR_CODE,
 				DISPATCH_DATE,
  				ORIGIN_TYPE,
  				ORIGIN_LOCATION_CODE,
  				ORIGIN_CODE,
  				ORIGIN_DESCR,
 				DESTINATION_LOCATION_CODE,
 				DESTINATION_CODE,
  				LTI_ID,
 				LOADING_DATE,
 				ORGANIZATION_ID,
 				TRAN_TYPE_CODE,
 				VEHICLE_REGISTRATION,
 				MODETRANS_CODE,
 				COMMENTS,
 				PERSON_CODE,
 				PERSON_OUC,
 				CERTIFING_TITLE,
 				TRANS_CONTRACTOR_CODE,
 				SUPPLIER1_OUC,
 				DRIVER_NAME,
 				LICENSE,
 				CURR_CONTAINER_NUMBER,
 				settings.COMPAS_STATION,
 				Full_coi,
 				COMM_CATEGORY_CODE,
 				COMM_CODE,
 				PCKKCODE,
 				ALLCODE,
 				QUALITY,
 				strNetTotal,
 				strGrossTotal,
 				UnitsLoaded,
 				UnitNet,
 				UnitGross,
 ]

			cursor.callproc('write_waybill.dispatch',(
				Response_Message,
				Response_Code,
				CURR_CODE,
				DISPATCH_DATE,
				ORIGIN_TYPE,
				ORIGIN_LOCATION_CODE,
				ORIGIN_CODE,
				ORIGIN_DESCR,
				DESTINATION_LOCATION_CODE,
				DESTINATION_CODE,
				LTI_ID,
				LOADING_DATE,
				ORGANIZATION_ID,
				TRAN_TYPE_CODE,
				VEHICLE_REGISTRATION,
				MODETRANS_CODE,
				COMMENTS,
				PERSON_CODE,
				PERSON_OUC,
				CERTIFING_TITLE,
				TRANS_CONTRACTOR_CODE,
				SUPPLIER1_OUC,
				DRIVER_NAME,
				LICENSE,
				CURR_CONTAINER_NUMBER,
				settings.COMPAS_STATION,
				Full_coi,
				COMM_CATEGORY_CODE,
				COMM_CODE,
				PCKKCODE,
				ALLCODE,
				QUALITY,
				strNetTotal,
				strGrossTotal,
				UnitsLoaded,
				UnitNet,
				UnitGross,
				empty
				)
				)
				
			if(	Response_Code.getvalue() == 'S'):
				pass
			else:
				all_ok =False			
				self.ErrorMessages +=str(loopNumber) + Full_coi+":"+Response_Message.getvalue() + " "
				self.ErrorCodes += str(loopNumber) + Full_coi+":"+ Response_Code.getvalue()+ " "
			
			print Response_Message.getvalue()
			print Response_Code.getvalue()
			
		if not all_ok:
			db.rollback()
		else:
			db.commit()
			
		cursor.close()
		db.close()
		
		return all_ok
