### -*- coding: utf-8 -*- ####################################################

from datetime import datetime

from django.test import TestCase
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404


import ets.models
import compas.models as compas_models
from ets.utils import import_stock, send_dispatched, send_received
from .utils import TestCaseMixin

class CompasTestCase(TestCase):
    
    #multi_db = True
    compas = 'ISBX002'
    fixtures = ('db_compas.json', 'warehouse.json')
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        call_command('loaddata', 'compas.json', verbosity=0, commit=False, database=self.compas)
    
    def test_sync_compas(self):
        
        self.assertEqual(ets.models.Compas.objects.count(), 1)
        self.assertEqual(compas_models.Place.objects.using(self.compas).count(), 3)
        self.assertEqual(ets.models.Location.objects.count(), 0)
        self.assertEqual(ets.models.Warehouse.objects.count(), 3)
        self.assertEqual(ets.models.Organization.objects.count(), 0)
        
        call_command('sync_compas')
        
        """Test place's update method"""
        self.assertEqual(ets.models.Location.objects.count(), 2)
        self.assertEqual(ets.models.Warehouse.objects.count(), 3)
        self.assertEqual(ets.models.Organization.objects.count(), 2)
        self.assertEqual(ets.models.Compas.objects.count(), 1)

        wh = ets.models.Warehouse.objects.get(pk='ISBX002')
        self.assertTupleEqual((wh.organization, wh.location, wh.compas) , 
                              (ets.models.Organization.objects.get(pk='WFP'), 
                               ets.models.Location.objects.get(pk='ISBX'),
                               ets.models.Compas.objects.get(pk=self.compas),))
        
        #Persons
        person = ets.models.Person.objects.get(pk=2)
        self.assertTupleEqual((person.organization, person.location, person.compas, person.username),
                              (ets.models.Organization.objects.get(pk='WFP'), 
                               ets.models.Location.objects.get(pk='ISBX'),
                               ets.models.Compas.objects.get(pk=self.compas),
                               'ISBX0020000586'))
        
        #test loss and damage types. The same story. It's stupid :)
        self.assertEqual(ets.models.LossDamageType.objects.count(), 4)
        
        """test stock update"""
        self.assertEqual(ets.models.StockItem.objects.count(), 7)
        stock_item = ets.models.StockItem.objects.get(pk='KARX025KARX0010000944801MIXMIXHEBCG1558')
        
        #Commodity name and category
        self.assertTupleEqual((stock_item.commodity.name, stock_item.commodity.category.pk), (u'WHEET', u'SED'))
        
        #After import we've got net --> number_of_units and quantity_net == 1
        self.assertTupleEqual((stock_item.number_of_units, stock_item.unit_weight_net), (1000, 1))
        
        #Update changed stock
        compas_models.EpicStock.objects.using(self.compas).filter(origin_id='testme0124').update(quantity_net=700)
        import_stock(self.compas)
        
        self.assertEqual(ets.models.StockItem.objects.get(pk='KARX025KARX0010000944801MIXMIXHEBCG1558').number_of_units, 700)
        
        #Deleted stock
        compas_models.EpicStock.objects.using(self.compas).filter(origin_id='testme0124').delete()
        import_stock(self.compas)
        
        self.assertEqual(ets.models.StockItem.objects.get(pk='KARX025KARX0010000944801MIXMIXHEBCG1558').number_of_units, 0)
        
        """Update orders"""
        order = ets.models.Order.objects.all()[0]
        self.assertEqual(order.warehouse, wh)
        self.assertEqual(order.location, ets.models.Location.objects.get(pk='ISBX'))
        self.assertEqual(order.consignee, ets.models.Organization.objects.get(pk='DOEAF'))
        
        #Test updated consignee's name
        self.assertEqual(ets.models.Organization.objects.get(pk='DOEAF').name, 'First consignee in our system')
        
        #Test order items
        self.assertEqual(order.items.count(), 1)
    
    
class SendCompasTestCase(TestCaseMixin, TestCase):
    
    def test_send_dispatched(self):
        
        def call_db_procedure(name, parameters, using):
            
            assert name == 'write_waybill.dispatch', "Wrong procedure's name"
            assert isinstance(parameters, tuple), "Parameters must be a tuple"
            assert using == self.compas, "Wrong compas"
            
        ets.utils.call_db_procedure = call_db_procedure
        
        waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        
        #Validate first waybill
        waybill.validated = True
        waybill.transport_dispach_signed_date = datetime.now()
        waybill.save()
        
        #Send all validated waybills to compas
        send_dispatched(waybill, self.compas)
        
        self.assertTrue(ets.models.Waybill.objects.get(pk="ISBX00211A").sent_compas)
        
        #Check compass logger
        logger = ets.models.CompasLogger.objects.get(waybill__pk='ISBX00211A')
        self.assertEqual(logger.status, ets.models.CompasLogger.SUCCESS)
    
    def test_dispatch_failure(self):
        
        def call_db_procedure(name, parameters, using):
            
            raise ValidationError("Test wrong message", code="E")
        
        ets.utils.call_db_procedure = call_db_procedure
        
        ets.models.Waybill.objects.filter(pk="ISBX00211A").update(validated=True, 
                                                        transport_dispach_signed_date=datetime.now())
        
        waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        
        #Send all validated waybills to compas
        send_dispatched(waybill, self.compas)
        
        self.assertFalse(waybill.sent_compas)
        self.assertFalse(waybill.validated)
        
        #Check compass logger
        logger = ets.models.CompasLogger.objects.get(waybill__pk='ISBX00211A')
        self.assertTupleEqual((logger.status, logger.message), (ets.models.CompasLogger.FAILURE, "Test wrong message"))
        
    def test_send_received(self):
        
        def call_db_procedure(name, parameters, using):
            assert name == 'write_waybill.receipt', "Wrong procedure's name"
            assert isinstance(parameters, tuple), "Parameters must be a tuple"
            assert using == self.compas, "Wrong compas"
        
        ets.utils.call_db_procedure = call_db_procedure
        
        waybill = ets.models.Waybill.objects.get(pk="ISBX00312A")
        
        #Validate first waybill
        waybill.receipt_validated = True
        waybill.receipt_signed_date = datetime.now()
        waybill.save()
        
        #Send all validated waybills to compas
        send_received(waybill, self.compas)
        
        self.assertTrue(ets.models.Waybill.objects.get(pk="ISBX00312A").receipt_sent_compas)
        
        #Check compass logger
        logger = ets.models.CompasLogger.objects.get(waybill__pk='ISBX00312A')
        self.assertEqual(logger.status, ets.models.CompasLogger.SUCCESS)
    
    def test_received_failure(self):
        
        def call_db_procedure(name, parameters, using):
            raise ValidationError("Test wrong message", code="E")
        
        ets.utils.call_db_procedure = call_db_procedure
        
        ets.models.Waybill.objects.filter(pk="ISBX00312A").update(receipt_validated=True, 
                                                                  receipt_signed_date=datetime.now())
        
        #Send all validated waybills to compas
        send_received(ets.models.Waybill.objects.get(pk="ISBX00312A"), self.compas)
        
        self.assertFalse(ets.models.Waybill.objects.get(pk="ISBX00312A").receipt_sent_compas)
        self.assertFalse(ets.models.Waybill.objects.get(pk="ISBX00312A").receipt_validated)
        
        #Check compass logger
        logger = ets.models.CompasLogger.objects.get(waybill__pk='ISBX00312A')
        self.assertTupleEqual((logger.status, logger.message), (ets.models.CompasLogger.FAILURE, "Test wrong message"))
        
