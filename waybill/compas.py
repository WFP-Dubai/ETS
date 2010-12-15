import cx_Oracle
from ets.waybill.models import *
from ets.waybill.forms import *
from ets.waybill.views import *
from ets.waybill.tools import *
from django.db import models
from django.db import connections
from django.conf import settings
import datetime

class compas_write:
	ErrorMessages = ''
	ErrorCodes = ''
	ConnectionString = settings.DATABASES[u'compas'][u'USER']+'/'+settings.DATABASES[u'compas'][u'PASSWORD']+u'@//'+ settings.DATABASES[u'compas'][u'HOST'] +u':1521/'+settings.COMPAS_STATION
	def __enter__(self):
		self.__db = cx_Oracle.Connection(ConnectionString)
		self.__cursor = self.__db.cursor()
		return self 
	def __exit__(self, type, value, traceback):
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
		try:
			db = cx_Oracle.Connection(self.ConnectionString)
			cursor = db.cursor()
			twoCont = False
			all_ok = True
			self.ErrorMessages = ''
			self.ErrorCodes = ''
			the_waybill = Waybill.objects.get(id=waybill_id)
			lineItems = the_waybill.loadingdetail_set.select_related()
			WB_CODE = the_waybill.waybillNumber
			receiverPerson  = EpicPerson.objects.get(person_pk = the_waybill.recipientName)
			recPersonOUC = receiverPerson.org_unit_code
			recPersonCode = receiverPerson.code
			arrival_date = unicode(the_waybill.recipientArrivalDate.strftime("%Y%m%d"))
			
			## check if containers = 2 & lines = 2
                        
			if lineItems.count() == 2:
                                if len(the_waybill.containerTwoNumber) > 0:
                                        twoCont = True
			codeLetter = u'A'
			#test if bulk or not
			isBulk = lineItems[0].siNo.isBulk()
			db.begin()
            
			for lineItem in lineItems:
				CURR_CODE=unicode(datetime.datetime.now().strftime('%y') +WB_CODE)
				if twoCont:
					CURR_CODE = unicode(datetime.datetime.now().strftime('%y') + codeLetter + WB_CODE)
					codeLetter = u'B'
                	
				goodUnits = unicode(lineItem.numberUnitsGood)
				if lineItem.numberUnitsDamaged > 0:
					damadgedUnits =unicode(lineItem.numberUnitsDamaged)
					damadgedReason = unicode(lineItem.unitsDamagedReason.compasRC.REASON)
				else:
					damadgedReason = u''
					damadgedUnits = u''
				if lineItem.numberUnitsLost:
					lostUnits =unicode(lineItem.numberUnitsLost)
					lossReason = unicode(lineItem.unitsLostReason.compasRC.REASON)
				else:
					lossReason = u''
					lostUnits = u''

				COI_CODE = unicode(lineItem.siNo.coi_code())			
				TheStockItems = EpicStock.objects.filter(origin_id__contains=COI_CODE)
				Full_coi= TheStockItems[0].origin_id
				COMM_CATEGORY_CODE = lineItem.siNo.COMM_CATEGORY_CODE
				COMM_CODE = lineItem.siNo.COMMODITY_CODE
				#get stock
				PCKKCODE = TheStockItems[0].package_code
				ALLCODE = TheStockItems[0].allocation_code
				QUALITY = TheStockItems[0].qualitycode #'G'
				Response_Message = cursor.var(cx_Oracle.STRING)
				Response_Message.setvalue(0,u' '*200)
				Response_Code = cursor.var(cx_Oracle.STRING)
				Response_Code.setvalue(0,u' '*2)
				print [Response_Message, Response_Code,CURR_CODE, recPersonOUC, recPersonCode, arrival_date, goodUnits,
                                        damadgedReason,damadgedUnits,lossReason,lostUnits,Full_coi,COMM_CATEGORY_CODE,COMM_CODE,PCKKCODE,ALLCODE,QUALITY]
				
				cursor.callproc(u'write_waybill.receipt',(Response_Message, Response_Code,CURR_CODE, recPersonOUC, recPersonCode, arrival_date, goodUnits,
                                        damadgedReason,damadgedUnits,lossReason,lostUnits,Full_coi,COMM_CATEGORY_CODE,COMM_CODE,PCKKCODE,ALLCODE,QUALITY))
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
			return all_ok
		except cx_Oracle.DatabaseError:
			print 'Issue with Connection'
			self.ErrorMessages = 'Problem with connection to COMPAS'
			return False
		except:
			print 'Issue with data'
			the_waybill = Waybill.objects.get(id=waybill_id)
			self.ErrorMessages = 'Problem with data of Waybill %s \n'%(the_waybill)
			return False
   
   
	def write_dispatch_waybill_compas(self,waybill_id):
		#try:
			db = cx_Oracle.Connection(self.ConnectionString)
			cursor = db.cursor()
			self.ErrorMessages = u''
			self.ErrorCodes = u''
			# gather wb info
			the_waybill = Waybill.objects.get(id=waybill_id)
			lineItems = the_waybill.loadingdetail_set.select_related()
			LTI= lineItems[0].siNo
			dispatch_person = EpicPerson.objects.get(person_pk = the_waybill.dispatcherName)
			# make dispatch remarks::::
			dispatch_remarks = the_waybill.dispatchRemarks
			CODE =  the_waybill.waybillNumber
			DOCUMENT_CODE = u'wb'
			DISPATCH_DATE=unicode(the_waybill.dateOfDispatch.strftime("%Y%m%d"))
			ORIGIN_TYPE=LTI.ORIGIN_TYPE
			ORIGIN_LOCATION_CODE=LTI.ORIGIN_LOCATION_CODE
			ORIGIN_CODE=LTI.ORIGIN_WH_CODE
			ORIGIN_DESCR=u''
			DESTINATION_LOCATION_CODE=LTI.DESTINATION_LOCATION_CODE
			DESTINATION_CODE=unicode(the_waybill.destinationWarehouse.ORG_CODE)
			PRO_ACTIVITY_CODE=u""
			ACTIVITY_OUC=u""
			LNDARRM_CODE=u""
			LTI_ID=LTI.LTI_ID
			LOADING_DATE=unicode(the_waybill.dateOfLoading.strftime("%Y%m%d"))
			ORGANIZATION_ID=LTI.CONSEGNEE_CODE
			TRAN_TYPE_CODE=the_waybill.transactionType
			TRAN_TYPE_DESCR=the_waybill.transportVehicleRegistration
			MODETRANS_CODE=the_waybill.transportType
			COMMENTS=	removeNonAsciiChars(dispatch_remarks)
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
			all_ok = True
			## For each lineItems
			# check if is bulk
			isBulk = lineItems[0].siNo.isBulk()

			## check if containers = 2 & lines = 2
			twoCont = False
			if lineItems.count() == 2:
				if len(the_waybill.containerTwoNumber) > 0:
					twoCont = True
			codeLetter = u'A'
			db.begin()
		
			for lineItem in lineItems:
				CURR_CODE=unicode(datetime.datetime.now().strftime('%y') +CODE)
				if twoCont:
					CURR_CODE = unicode(datetime.datetime.now().strftime('%y') + codeLetter + CODE)
					codeLetter = u'B'
					CONTAINER_NUMBER=unicode(the_waybill.containerTwoNumber)		
					
				if lineItem.loadingDetailSentToCompas:
					pass
				else:
					CURR_CONTAINER_NUMBER=CONTAINER_NUMBER	
					COMM_CATEGORY_CODE = lineItem.siNo.COMM_CATEGORY_CODE
					COMM_CODE = lineItem.siNo.COMMODITY_CODE
					COI_CODE = unicode(lineItem.siNo.coi_code())			
					#get stock
					TheStockItems = EpicStock.objects.filter(origin_id__contains=COI_CODE)
					PCKKCODE = TheStockItems[0].package_code
					ALLCODE = TheStockItems[0].allocation_code
					QUALITY = TheStockItems[0].qualitycode #'G'
					UnitsLoaded = lineItem.numberUnitsLoaded
					strUnitsLoaded =  u'%.3f' % UnitsLoaded
					UnitNet= lineItem.siNo.UNIT_WEIGHT_NET
					UnitGross = lineItem.siNo.UNIT_WEIGHT_GROSS
					strUnitNet =  u'%.3f' % UnitNet
					strUnitGross =  u'%.3f' % UnitGross
					NetTotal =(UnitNet * UnitsLoaded) / 1000
					strNetTotal = u'%.3f' % NetTotal
					GrossTotal = (UnitGross * UnitsLoaded) / 1000
					strGrossTotal = u'%.3f' % GrossTotal
					Response_Message = cursor.var(cx_Oracle.STRING)
					Response_Message.setvalue(0,u'x'*80)
					Response_Code = cursor.var(cx_Oracle.STRING)
					Response_Code.setvalue(0,u'x'*2)
					Full_coi= TheStockItems[0].origin_id
					empty = u''
					
					if isBulk:
						pass# manage bulk..... set number of items to 1 and take the units and put them into NetTotal & Gross Total
						strUnitsLoaded=u'1.000'
						strUnitNet = u''
						strUnitGross =  u''
						strNetTotal = u'%.3f' % UnitsLoaded
						strGrossTotal = u'%.3f' % UnitsLoaded
						
					printlist( [Response_Message,Response_Code,CURR_CODE,DISPATCH_DATE,ORIGIN_TYPE,ORIGIN_LOCATION_CODE,ORIGIN_CODE,
						ORIGIN_DESCR,DESTINATION_LOCATION_CODE,DESTINATION_CODE,LTI_ID,LOADING_DATE,ORGANIZATION_ID,TRAN_TYPE_CODE,VEHICLE_REGISTRATION,MODETRANS_CODE,
						COMMENTS,PERSON_CODE,PERSON_OUC,CERTIFING_TITLE,TRANS_CONTRACTOR_CODE,SUPPLIER1_OUC,DRIVER_NAME,LICENSE,CURR_CONTAINER_NUMBER,settings.COMPAS_STATION,
						Full_coi,COMM_CATEGORY_CODE,COMM_CODE,PCKKCODE,ALLCODE,QUALITY,strNetTotal,strGrossTotal,strUnitsLoaded,strUnitNet,strUnitGross,empty])
					cursor.callproc(u'write_waybill.dispatch',(Response_Message,Response_Code,CURR_CODE,DISPATCH_DATE,ORIGIN_TYPE,ORIGIN_LOCATION_CODE,ORIGIN_CODE,
						ORIGIN_DESCR,DESTINATION_LOCATION_CODE,DESTINATION_CODE,LTI_ID,LOADING_DATE,ORGANIZATION_ID,TRAN_TYPE_CODE,VEHICLE_REGISTRATION,MODETRANS_CODE,
						COMMENTS,PERSON_CODE,PERSON_OUC,CERTIFING_TITLE,TRANS_CONTRACTOR_CODE,SUPPLIER1_OUC,DRIVER_NAME,LICENSE,CURR_CONTAINER_NUMBER,settings.COMPAS_STATION,
						Full_coi,COMM_CATEGORY_CODE,COMM_CODE,PCKKCODE,ALLCODE,QUALITY,strNetTotal,strGrossTotal,strUnitsLoaded,strUnitNet,strUnitGross,u''))
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
		#except cx_Oracle.DatabaseError,e:
			errorObj, = e.args
			if errorObj.code == 12514:
				print 'Issue with Connection' + str(errorObj.code)
				self.ErrorMessages = 'Problem with connection to COMPAS'
				return False
			else:
				print 'Issue with data'
				the_waybill = Waybill.objects.get(id=waybill_id)
				self.ErrorMessages = 'Problem with data of Waybill %s: %s \n'%(the_waybill,str(errorObj.code))
				return False
		#except Exception as e:
			print 'Issue with data'
			the_waybill = Waybill.objects.get(id=waybill_id)
			self.ErrorMessages = 'Problem with data of Waybill %s \n'%(the_waybill) + self.ErrorMessages
			return False

def printlist(list):
	for item in list:
		print item