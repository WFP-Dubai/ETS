import cx_Oracle
from ets.waybill.models import *
from ets.waybill.forms import *
from ets.waybill.views import *
from django.db import models
from django.db import connections
from django.conf import settings

class compas_write:
	ErrorMessages = ''
	ErrorCodes = ''

	def __enter__(self):
		self.__db = cx_Oracle.Connection("TESTJERX001/TESTJERX001@//10.11.216.4:1521/JERX001")
		self.__cursor = self.__db.cursor()
		return self 
	def __exit__(self, type, value, traceback):
   		self.__cursor.close()
		self.__db.close()

	def write_receipt_waybill_compas(self,waybill_id):
		db = cx_Oracle.Connection("TESTJERX001/TESTJERX001@//10.11.216.4:1521/JERX001")
		cursor =  db.cursor()#connections['compas'].cursor()		
		self.ErrorMessages = ''
		self.ErrorCodes = ''
		the_waybill = Waybill.objects.get(id=waybill_id)
		lineItems = the_waybill.loadingdetail_set.select_related()
		WB_CODE = the_waybill.waybillNumber
		receiverPerson  = EpicPerson.objects.get(person_pk = the_waybill.recipientName)
		recPersonOUC = receiverPerson.org_unit_code
		recPersonCode = receiverPerson.code
		arrival_date = the_waybill.recipientArrivalDate
		all_ok = True
		db.begin()
	
		for lineItem in lineItems:
			goodUnits = lineItem.numberUnitsGood
			damadgedUnits =lineItem.numberUnitsDamaged
			damadgedReason = lineItem.unitsDamagedReason.compasCode
			lostUnits =lineItem.numberUnitsLost
			lossReason = lineItem.unitsLostReason.compasCode
			
			Response_Message = cursor.var(cx_Oracle.STRING)
			Response_Message.setvalue(0,' '*200)
			Response_Code = cursor.var(cx_Oracle.STRING)
			Response_Code.setvalue(0,' '*2)
			Full_coi= TheStockItems[0].origin_id

			cursor.callproc('write_waybill.dispatch',(
				Response_Message,
				Response_Code,
				WB_CODE,
				recPersonOUC,
				recPersonCode,
				arrival_date,
				goodUnits,
				damadgedReason,
				damadgedUnits,
				lossReason,
				lostUnits
				))
				
			if(	Response_Code.getvalue() == 'S'):
				pass
			else:
				all_ok =False			
				self.ErrorMessages += Full_coi+":"+Response_Message.getvalue() + " "
				self.ErrorCodes += Full_coi+":"+ Response_Code.getvalue()+ " "
		
		if not all_ok:
			db.rollback()
		else:
			db.commit()

			
		cursor.close()
		db.close()

		

	def write_dispatch_waybill_compass(self,waybill_id):
		db = cx_Oracle.Connection("TESTJERX001/TESTJERX001@//10.11.216.4:1521/JERX001")
		cursor =  db.cursor()#connections['compas'].cursor()		
		self.ErrorMessages = ''
		self.ErrorCodes = ''
		
		# gather wb info
		the_waybill = Waybill.objects.get(id=waybill_id)
		lineItems = the_waybill.loadingdetail_set.select_related()
		LTI= lineItems[0].siNo
		dispatch_person = EpicPerson.objects.get(person_pk = the_waybill.dispatcherName)
		# make dispatch remarks::::
		dispatch_remarks = the_waybill.dispatchRemarks
		CODE = the_waybill.waybillNumber
		DOCUMENT_CODE = 'wb'
		DISPATCH_DATE=the_waybill.dateOfDispatch.strftime("%Y%m%d")
		ORIGIN_TYPE=LTI.ORIGIN_TYPE
		ORIGIN_LOCATION_CODE=LTI.ORIGIN_LOCATION_CODE
		ORIGIN_CODE=LTI.ORIGIN_WH_CODE
		ORIGIN_DESCR=''
		DESTINATION_LOCATION_CODE=LTI.DESTINATION_LOCATION_CODE
		DESTINATION_CODE=str(the_waybill.destinationWarehouse.ORG_CODE)
		PRO_ACTIVITY_CODE=""
		ACTIVITY_OUC=""
		LNDARRM_CODE=""
		LTI_ID=LTI.LTI_ID
		LOADING_DATE=the_waybill.dateOfLoading.strftime("%Y%m%d")
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
		db.begin()
	
		for lineItem in lineItems:
			COMM_CATEGORY_CODE = lineItem.siNo.COMM_CATEGORY_CODE
			COMM_CODE = lineItem.siNo.COMMODITY_CODE
			COI_CODE = lineItem.siNo.coi_code()			
			#get stock
			TheStockItems = EpicStock.objects.filter(origin_id__contains=COI_CODE)
			PCKKCODE = TheStockItems[0].package_code
			ALLCODE = TheStockItems[0].allocation_code
			QUALITY = TheStockItems[0].qualitycode #'G'
			UnitsLoaded = lineItem.numberUnitsLoaded
			UnitNet= lineItem.siNo.UNIT_WEIGHT_NET
			UnitGross = lineItem.siNo.UNIT_WEIGHT_GROSS
			
			NetTotal =(UnitNet * UnitsLoaded) / 1000
			strNetTotal = "%.3f" % NetTotal
			GrossTotal = (UnitGross * UnitsLoaded) / 1000
			strGrossTotal = "%.3f" % GrossTotal

			Response_Message = cursor.var(cx_Oracle.STRING)
			Response_Message.setvalue(0,' '*200)
			Response_Code = cursor.var(cx_Oracle.STRING)
			Response_Code.setvalue(0,' '*2)
			Full_coi= TheStockItems[0].origin_id


 			print [CODE,
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
 				CONTAINER_NUMBER,
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
				CODE,
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
				CONTAINER_NUMBER,
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
				''
				)
				)
				
			if(	Response_Code.getvalue() == 'S'):
				pass
			else:
				all_ok =False			
				self.ErrorMessages += Full_coi+":"+Response_Message.getvalue() + " "
				self.ErrorCodes += Full_coi+":"+ Response_Code.getvalue()+ " "
			
			print Response_Message.getvalue()
			print Response_Code.getvalue()
			
		if not all_ok:
			db.rollback()
		else:
			db.commit()
			
		cursor.close()
		db.close()
		
		return all_ok
