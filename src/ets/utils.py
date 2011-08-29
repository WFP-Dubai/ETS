from datetime import datetime

from django.db import connections
from django.db.utils import DatabaseError

import models as ets_models


def update_compas(using):
    
    #send_dispatched(using)
    #send_received(using)
    
    #Update places
    ets_models.Place.update(using)
    
    #Update persons
    ets_models.CompasPerson.update(using)
    
    #Update stocks
    ets_models.EpicStock.update(using)
    
    #Update loss/damage types
    ets_models.LossDamageType.update(using)
    
    #Update orders
    ets_models.LtiOriginal.update(using)


def send_dispatched(using):
    connection = connections[using]
    cursor = connection.cursor()
    for waybill in ets_models.Waybill.objects.filter(transport_dispach_signed_date__lte=datetime.now(), 
                                                     validated=True, sent_compas=False):
        try:
            #===========================================================================================================
            # self.ErrorMessages = u''
            # self.ErrorCodes = u''
            #===========================================================================================================
            empty = u''
            # gather wb info
            loading_details = waybill.loading_details.all()
            
            CONTAINER_NUMBER = waybill.container_one_number
            all_ok = True

            ## check if containers = 2 & lines = 2
            twoCont = loading_details.count() == 2 and waybill.container_two_number
            #connecion.begin()
            codeLetter = u'A'

            for index, loading in enumerate( loading_details ):
                
                #Setting the waybill number for compas
                CURR_CODE = u"%s%s" % (datetime.datetime.now().strftime( '%y' ), waybill.pk)
                if twoCont:
                    CURR_CODE = u"%s%s%s" % (datetime.datetime.now().strftime( '%y' ), codeLetter, waybill.pk)
                    codeLetter = u'B'
                    if index == 1:
                        CONTAINER_NUMBER = waybill.containerTwoNumber
                
                if loading.sent_compas:
                    pass
                else:
                    
                    Response_Message = cursor.var( cx_Oracle.STRING )
                    Response_Message.setvalue( 0, u' ' * 80 )
                    
                    Response_Code = cursor.var( cx_Oracle.STRING )
                    Response_Code.setvalue( 0, u'x' * 2 )
                    
                    is_bulk = loading.stock_item.is_bulk
                    
                    cursor.callproc( u'write_waybill.dispatch', ( 
                            Response_Message, Response_Code,
                            CURR_CODE, 
                            unicode( waybill.dispatch_date.strftime( "%Y%m%d" ) ), 
                            waybill.order.origin_type, 
                            waybill.order.warehouse.location.pk, 
                            waybill.order.warehouse.pk,
                            empty, 
                            waybill.order.location.pk, 
                            waybill.order.consignee.pk, 
                            waybill.order.pk, 
                            unicode( waybill.loading_date.strftime( "%Y%m%d" ) ),
                            waybill.order.consignee.pk, 
                            waybill.transaction_type, 
                            waybill.transport_vehicle_registration, 
                            waybill.transport_type,
                            waybill.dispatch_remarks, 
                            waybill.dispatcher_person.code, 
                            waybill.dispatcher_person.compas, 
                            waybill.dispatcher_person.title, 
                            waybill.order.transport_code, 
                            waybill.order.transport_ouc,
                            waybill.transport_driver_name, 
                            waybill.transport_driver_licence, 
                            CONTAINER_NUMBER, 
                            using,
                            loading.stock_item.pk, 
                            loading.stock_item.commodity.category.pk, 
                            loading.stock_item.commodity.pk, 
                            loading.stock_item.package.pk, 
                            loading.stock_item.allocation_code, 
                            loading.stock_item.quality_code,
                            
                            u'%.3f' % loading.calculate_total_net(), 
                            u'%.3f' % loading.calculate_total_gross(), 
                            u'%.3f' % (1 if is_bulk else loading.number_of_units), 
                            u'' if is_bulk else u'%.3f' % loading.stock_item.unit_weight_net, 
                            u'' if is_bulk else u'%.3f' % loading.stock_item.unit_weight_gross, 
                            
                            empty, empty, empty )
                    )

                    if( Response_Code.getvalue() == 'S' ):
                        pass
                    else:
                        all_ok = False
                        error_first_line = Response_Message.getvalue().split( '\n' )[0]
                        self.ErrorMessages += loading.stock_item.pk + ":" + error_first_line + " "
                        self.ErrorCodes += loading.stock_item.pk + ":" + Response_Code.getvalue() + " "
                    print Response_Message.getvalue()
                    print Response_Code.getvalue()
            if not all_ok:
                db.rollback()
            else:
                db.commit()
            cursor.close()
            db.close()
            return all_ok
        except DatabaseError, e:
            errorObj, = e.args
            if errorObj.code == 12514:
                print 'Issue with Connection' + str( errorObj.code )
                self.ErrorMessages = _('Problem with connection to COMPAS')
                return False
            else:
                print 'Issue with data1'
                self.ErrorMessages = _("Problem with data of Waybill  %(waybill)s: %(errorcode)s \n") % {"waybill": waybill,"errorcode": errorObj.code }
                return False
        except Exception as e:
            print 'Issue with data2'
            print self.ErrorMessages
            
            self.ErrorMessages = _("Problem with data of Waybill %(waybill)s \n %(errormsg)s") % { "waybill": waybill, "errormsg": self.ErrorMessages }
            
            return False


def send_received(using):
    for reception in ets_models.ReceiptWaybill.objects.filter(signed_date__lte=datetime.now(), 
                                                            validated=True, sent_compas=False):
            pass
