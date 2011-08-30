from datetime import datetime

from django.db import connections, transaction
from django.db.utils import DatabaseError

import models as ets_models


def update_compas(using):
    
    send_dispatched(using)
    
    send_received(using)
    
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
    for waybill in ets_models.Waybill.objects.filter(transport_dispach_signed_date__lte=datetime.now(), 
                                                     validated=True, sent_compas=False,
                                                     order__warehouse__compas__pk=using):
        with transaction.commit_on_success(using=using) as tr:
            
            CURR_CODE = u"%s%s" % (datetime.datetime.now().strftime( '%y' ), waybill.pk)
            
            CONTAINER_NUMBER = waybill.container_one_number
    
            special_case = waybill.loading_details.count() == 2 and waybill.container_two_number
            code_letter = u'A'
    
            for index, loading in enumerate( waybill.loading_details.all() ):
                
                if special_case:
                    CURR_CODE = u"%s%s%s" % (datetime.datetime.now().strftime( '%y' ), code_letter, waybill.pk)
                    code_letter = u'B'
                    if index == 1:
                        CONTAINER_NUMBER = waybill.container_two_number
            
                is_bulk = loading.stock_item.is_bulk
                
                call_db_procedure('write_waybill.dispatch', (
                    CURR_CODE, 
                    waybill.dispatch_date.strftime( "%Y%m%d" ), 
                    waybill.order.origin_type, 
                    waybill.order.warehouse.location.pk, 
                    waybill.order.warehouse.pk,
                    '', 
                    waybill.order.location.pk, 
                    waybill.order.consignee.pk, 
                    waybill.order.pk, 
                    waybill.loading_date.strftime( "%Y%m%d" ),
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
                    
                    '', '', '' 
                ), tr.using)
            
            waybill.sent_compas = True
            waybill.save()

def send_received(using):
    for reception in ets_models.ReceiptWaybill.objects.filter(signed_date__lte=datetime.now(), 
                                                              validated=True, sent_compas=False,
                                                              waybill__destination__compas__pk=using):
        waybill = reception.waybill
        with transaction.commit_on_success(using=using) as tr:
            
            CURR_CODE = u"%s%s" % (datetime.datetime.now().strftime( '%y' ), waybill.pk)

            ## check if containers = 2 & lines = 2
            special_case = waybill.loading_details.count() == 2 and waybill.container_two_number
            code_letter = u'A'
            
            for loading in waybill.loading_details.all():
                
                if special_case:
                    CURR_CODE = u"%s%s%s" % (datetime.datetime.now().strftime( '%y' ), code_letter, waybill.pk)
                    code_letter = u'B'
                
                call_db_procedure('write_waybill.receipt', (
                    CURR_CODE, 
                    reception.person.compas.pk, 
                    reception.person.code, 
                    waybill.arrival_date.strftime("%Y%m%d"),
                    loading.number_units_good, 
                    loading.units_damaged_reason and loading.units_damaged_reason.cause or '', 
                    loading.number_units_damaged or '', 
                    loading.units_lost_reason and loading.units_lost_reason.cause or '', 
                    loading.number_units_lost or '', 
                    loading.stock_item.pk, 
                    loading.stock_item.commodity.category.pk,
                    loading.stock_item.commodity.pk, 
                    loading.stock_item.package.pk, 
                    loading.stock_item.allocation_code, 
                    loading.stock_item.quality_code
                ), tr.using)
                
        waybill.sent_compas = True
        waybill.save()
        

def call_db_procedure(name, parameters, using):
    import cx_Oracle
    cursor = connections[using].cursor()
    Response_Message = cursor.var( cx_Oracle.STRING )
    Response_Message.setvalue( 0, u' ' * 200 )
    Response_Code = cursor.var( cx_Oracle.STRING )
    Response_Code.setvalue( 0, u' ' * 2 )
    
    cursor.callproc( name, (Response_Message, Response_Code,)+parameters)
