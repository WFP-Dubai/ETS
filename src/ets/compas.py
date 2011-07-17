import cx_Oracle
from ets import models as ets_models
from ets.tools import removeNonAsciiChars
from django.conf import settings #@Reimport
import datetime #@Reimport 

class compas_write:
    ErrorMessages = ''
    ErrorCodes = ''
    ConnectionString = settings.DATABASES[u'compas'][u'USER'] + '/' + settings.DATABASES[u'compas'][u'PASSWORD'] + u'@//' + settings.DATABASES[u'compas'][u'HOST'] + u':1521/' + settings.COMPAS_STATION




    def write_dispatch_waybill_compas( self, waybill_id ):
        try:
            db = cx_Oracle.Connection( self.ConnectionString )
            cursor = db.cursor()
            self.ErrorMessages = u''
            self.ErrorCodes = u''
            empty = u''
            # gather wb info
            the_waybill = ets_models.Waybill.objects.get( id = waybill_id )
            lineItems = the_waybill.loadingdetail_set.select_related()
            LTI = lineItems[0].order_item.lti_item
            DISPATCH_PERSON = ets_models.EpicPerson.objects.get( person_pk = the_waybill.dispatcherName )
            # make dispatch remarks::::
            DISPATCH_REMARKS = the_waybill.dispatchRemarks
            CODE = the_waybill.waybillNumber
#            DOCUMENT_CODE = u'wb'
            DISPATCH_DATE = unicode( the_waybill.dateOfDispatch.strftime( "%Y%m%d" ) )
            ORIGIN_TYPE = LTI.origin_type
            ORIGIN_LOCATION_CODE = LTI.origin_location_code
            ORIGIN_CODE = LTI.origin_wh_code
            ORIGIN_DESCR = u''
            DESTINATION_LOCATION_CODE = LTI.destination_location_code
            DESTINATION_CODE = unicode( the_waybill.destinationWarehouse.org_code )
#            PRO_ACTIVITY_CODE = u""
#            ACTIVITY_OUC = u""
#            LNDARRM_CODE = u""
            LTI_ID = LTI.lti_id
            LOADING_DATE = unicode( the_waybill.dateOfLoading.strftime( "%Y%m%d" ) )
            ORGANIZATION_ID = LTI.consegnee_code
            TRAN_TYPE_CODE = the_waybill.transactionType
#            TRAN_TYPE_DESCR = the_waybill.transportVehicleRegistration
            MODETRANS_CODE = the_waybill.transportType
            COMMENTS = removeNonAsciiChars( DISPATCH_REMARKS )
            PERSON_CODE = DISPATCH_PERSON.code
            PERSON_OUC = DISPATCH_PERSON.org_unit_code
            CERTIFING_TITLE = DISPATCH_PERSON.title
            TRANS_CONTRACTOR_CODE = LTI.transport_code
            SUPPLIER1_OUC = LTI.transport_ouc
            DRIVER_NAME = the_waybill.transportDriverName
            LICENSE = the_waybill.transportDriverLicenceID
            VEHICLE_REGISTRATION = the_waybill.transportVehicleRegistration
#            TRAILER_PLATE = the_waybill.transportTrailerRegistration
            CONTAINER_NUMBER = the_waybill.containerOneNumber
            all_ok = True
            ## For each lineItems
            # check if is bulk
            is_bulk = lineItems[0].siNo.is_bulk()

            ## check if containers = 2 & lines = 2
            twoCont = False
            if lineItems.count() == 2:
                if len( the_waybill.containerTwoNumber ) > 0:
                    twoCont = True
            codeLetter = u'A'
            db.begin()

            for index, lineItem in enumerate( lineItems ):
                #Setting the waybill number for compas
                CURR_CODE = unicode( datetime.datetime.now().strftime( '%y' ) + CODE )
                if twoCont:
                    CURR_CODE = unicode( datetime.datetime.now().strftime( '%y' ) + codeLetter + CODE )
                    codeLetter = u'B'
                    if index == 1:
                        CONTAINER_NUMBER = unicode( the_waybill.containerTwoNumber )
                if lineItem.loadingDetailSentToCompas:
                    pass
                else:
                    CURR_CONTAINER_NUMBER = CONTAINER_NUMBER
                    LTI_ITEM = lineItem.siNo
                    COMM_CATEGOTY_CODE = LTI_ITEM.comm_category_code
                    COMM_CODE = LTI_ITEM.commodity_code
                    #fix coi
                    COI_CODE = unicode( LTI_ITEM.coi_code() )
                    #get Fix here... chage to stock...
                    TheStockItem = lineItem.stock_item
                    PCKKCODE = TheStockItem.package_code
                    ALLCODE = TheStockItem.allocation_code
                    QUALITY = TheStockItem.qualitycode #'G'
                    UnitsLoaded = lineItem.numberUnitsLoaded
                    strUnitsLoaded = u'%.3f' % UnitsLoaded
                    UnitNet = LTI_ITEM.unit_weight_net
                    UnitGross = LTI_ITEM.unit_weight_gross
                    strUnitNet = u'%.3f' % UnitNet
                    strUnitGross = u'%.3f' % UnitGross
                    NetTotal = ( UnitNet * UnitsLoaded ) / 1000
                    strNetTotal = u'%.3f' % NetTotal
                    GrossTotal = ( UnitGross * UnitsLoaded ) / 1000
                    if GrossTotal > TheStockItem.quantity_gross:
                        GrossTotal = TheStockItem.quantity_gross
                    strGrossTotal = u'%.3f' % GrossTotal
                    Response_Message = cursor.var( cx_Oracle.STRING )
                    Response_Message.setvalue( 0, u' ' * 80 )
                    Response_Code = cursor.var( cx_Oracle.STRING )
                    Response_Code.setvalue( 0, u'x' * 2 )
                    Full_coi = TheStockItem.origin_id
                    LOSSTYPE = empty
                    LOSSREASON = empty
                    ODAID = empty

                    if is_bulk:
                        # manage bulk..... set number of items to 1 and take the units and put them into NetTotal & Gross Total
                        strUnitsLoaded = u'1.000'
                        strUnitNet = u''
                        strUnitGross = u''
                        strNetTotal = u'%.3f' % UnitsLoaded
                        strGrossTotal = u'%.3f' % UnitsLoaded

                    print "\n".join([
                        Response_Message, Response_Code, CURR_CODE, DISPATCH_DATE, ORIGIN_TYPE, ORIGIN_LOCATION_CODE, 
                        ORIGIN_CODE, ORIGIN_DESCR, DESTINATION_LOCATION_CODE, DESTINATION_CODE, LTI_ID, LOADING_DATE, 
                        ORGANIZATION_ID, TRAN_TYPE_CODE, VEHICLE_REGISTRATION, MODETRANS_CODE, COMMENTS, PERSON_CODE, 
                        PERSON_OUC, CERTIFING_TITLE, TRANS_CONTRACTOR_CODE, SUPPLIER1_OUC, DRIVER_NAME, LICENSE, 
                        CURR_CONTAINER_NUMBER, settings.COMPAS_STATION, Full_coi, COMM_CATEGOTY_CODE, COMM_CODE, 
                        PCKKCODE, ALLCODE, QUALITY, strNetTotal, strGrossTotal, strUnitsLoaded, strUnitNet, 
                        strUnitGross, empty
                    ])

                    cursor.callproc( u'write_waybill.dispatch', ( Response_Message, Response_Code,
                                                                  CURR_CODE, DISPATCH_DATE, ORIGIN_TYPE, ORIGIN_LOCATION_CODE, ORIGIN_CODE,
                                                                  ORIGIN_DESCR, DESTINATION_LOCATION_CODE, DESTINATION_CODE, LTI_ID, LOADING_DATE,
                                                                  ORGANIZATION_ID, TRAN_TYPE_CODE, VEHICLE_REGISTRATION, MODETRANS_CODE,
                                                                  COMMENTS, PERSON_CODE, PERSON_OUC, CERTIFING_TITLE, TRANS_CONTRACTOR_CODE, SUPPLIER1_OUC,
                                                                  DRIVER_NAME, LICENSE, CURR_CONTAINER_NUMBER, settings.COMPAS_STATION,
                                                                  Full_coi, COMM_CATEGOTY_CODE, COMM_CODE, PCKKCODE, ALLCODE, QUALITY,
                                                                  strNetTotal, strGrossTotal, strUnitsLoaded, strUnitNet, strUnitGross, ODAID, LOSSTYPE, LOSSREASON )
                    )

                    if( Response_Code.getvalue() == 'S' ):
                        pass
                    else:
                        all_ok = False
                        error_first_line = Response_Message.getvalue().split( '\n' )[0]
                        self.ErrorMessages += Full_coi + ":" + error_first_line + " "
                        self.ErrorCodes += Full_coi + ":" + Response_Code.getvalue() + " "
                    print Response_Message.getvalue()
                    print Response_Code.getvalue()
            if not all_ok:
                db.rollback()
            else:
                db.commit()
            cursor.close()
            db.close()
            return all_ok
        except cx_Oracle.DatabaseError, e:
            errorObj, = e.args
            if errorObj.code == 12514:
                print 'Issue with Connection' + str( errorObj.code )
                self.ErrorMessages = 'Problem with connection to COMPAS'
                return False
            else:
                print 'Issue with data1'
                the_waybill = ets_models.Waybill.objects.get( id = waybill_id )
                self.ErrorMessages = 'Problem with data of Waybill %s: %s \n' % ( the_waybill, str( errorObj.code ) )
                return False
        except Exception as e:
            print 'Issue with data2'
            the_waybill = ets_models.Waybill.objects.get( id = waybill_id )
            print self.ErrorMessages
            self.ErrorMessages = 'Problem with data of Waybill %s \n' % ( the_waybill ) + self.ErrorMessages
            return False



    def write_receipt_waybill_compas( self, waybill_id ):
        try:
            db = cx_Oracle.Connection( self.ConnectionString )
            cursor = db.cursor()
            twoCont = False
            all_ok = True
            self.ErrorMessages = ''
            self.ErrorCodes = ''
            the_waybill = ets_models.Waybill.objects.get( id = waybill_id )
            lineItems = the_waybill.loadingdetail_set.select_related()
            WB_CODE = the_waybill.waybillNumber
            receiverPerson = ets_models.EpicPerson.objects.get( person_pk = the_waybill.recipientName )
            recPersonOUC = receiverPerson.org_unit_code
            recPersonCode = receiverPerson.code
            arrival_date = unicode( the_waybill.recipientArrivalDate.strftime( "%Y%m%d" ) )

            ## check if containers = 2 & lines = 2

            if lineItems.count() == 2:
                                if len( the_waybill.containerTwoNumber ) > 0:
                                        twoCont = True
            codeLetter = u'A'

            db.begin()

            for lineItem in lineItems:
                CURR_CODE = unicode( datetime.datetime.now().strftime( '%y' ) + WB_CODE )
                if twoCont:
                    CURR_CODE = unicode( datetime.datetime.now().strftime( '%y' ) + codeLetter + WB_CODE )
                    codeLetter = u'B'
                    if index == 1:
                        CONTAINER_NUMBER = unicode( the_waybill.containerTwoNumber )
                
                goodUnits = unicode( lineItem.numberUnitsGood )
                if lineItem.numberUnitsDamaged > 0:
                    damadgedUnits = unicode( lineItem.numberUnitsDamaged )
                    damadgedReason = unicode( lineItem.unitsDamagedReason.compasRC.REASON )
                else:
                    damadgedReason = u''
                    damadgedUnits = u''
                if lineItem.numberUnitsLost:
                    lostUnits = unicode( lineItem.numberUnitsLost )
                    lossReason = unicode( lineItem.unitsLostReason.compasRC.REASON )
                else:
                    lossReason = u''
                    lostUnits = u''

                TheStockItem = lineItem.stock_item
                Full_coi = TheStockItem.origin_id
                comm_category_code = lineItem.siNo.comm_category_code
                COMM_CODE = lineItem.siNo.commodity_code

                PCKKCODE = TheStockItem.package_code
                ALLCODE = TheStockItem.allocation_code
                QUALITY = TheStockItem.qualitycode
                Response_Message = cursor.var( cx_Oracle.STRING )
                Response_Message.setvalue( 0, u' ' * 200 )
                Response_Code = cursor.var( cx_Oracle.STRING )
                Response_Code.setvalue( 0, u' ' * 2 )
                print [Response_Message, Response_Code, CURR_CODE, recPersonOUC, recPersonCode, arrival_date, goodUnits,
                                        damadgedReason, damadgedUnits, lossReason, lostUnits, Full_coi, comm_category_code, COMM_CODE, PCKKCODE, ALLCODE, QUALITY]

                cursor.callproc( u'write_waybill.receipt', ( Response_Message, Response_Code, CURR_CODE, recPersonOUC, recPersonCode, arrival_date,
                                                             goodUnits, damadgedReason, damadgedUnits, lossReason, lostUnits, Full_coi, comm_category_code,
                                                             COMM_CODE, PCKKCODE, ALLCODE, QUALITY ) )
                if( Response_Code.getvalue() == 'S' ):
                    pass
                else:
                    all_ok = False
                    self.ErrorMessages += Full_coi + ":" + Response_Message.getvalue() + " "
                    self.ErrorCodes += Full_coi + ":" + Response_Code.getvalue() + " "

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
            the_waybill = ets_models.Waybill.objects.get( id = waybill_id )
            self.ErrorMessages = 'Problem with data of Waybill %s \n' % ( the_waybill )
            return False


#=======================================================================================================================
# def printlist( list ):
#    for item in list:
#        print item
#=======================================================================================================================
