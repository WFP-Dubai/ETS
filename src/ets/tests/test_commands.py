### -*- coding: utf-8 -*- ####################################################

from django.test import TestCase
from django.core.management import call_command

import ets.models

class CommandTestCase(TestCase):
    
    #multi_db = True
    compas = 'dev_compas'
    fixtures = ('db_compas.json',)
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        call_command('loaddata', 'compas.json', verbosity=0, commit=False, database=self.compas)
    
    def test_sync_compas(self):
        
        self.assertEqual(ets.models.Compas.objects.count(), 1)
        self.assertEqual(ets.models.Place.objects.using(self.compas).count(), 3)
        self.assertEqual(ets.models.Location.objects.count(), 0)
        self.assertEqual(ets.models.Warehouse.objects.count(), 0)
        self.assertEqual(ets.models.Organization.objects.count(), 0)
        
        call_command('sync_compas')
        
        """Test place's update method"""
        self.assertEqual(ets.models.Location.objects.count(), 2)
        self.assertEqual(ets.models.Warehouse.objects.count(), 3)
        self.assertEqual(ets.models.Organization.objects.count(), 1)
        self.assertEqual(ets.models.Compas.objects.count(), 1)

        wh = ets.models.Warehouse.objects.get(pk='ISBX002')
        self.assertTupleEqual((wh.organization, wh.location, wh.compas) , 
                              (ets.models.Organization.objects.get(pk='DOEAF'), 
                               ets.models.Location.objects.get(pk='ISBX'),
                               ets.models.Compas.objects.get(pk=self.compas),))
        
        #Persons
        person = ets.models.Person.objects.get(pk="ISBX0020000586")
        self.assertTupleEqual((person.organization, person.location, person.compas, person.user.username),
                              (ets.models.Organization.objects.get(pk='DOEAF'), 
                               ets.models.Location.objects.get(pk='ISBX'),
                               ets.models.Compas.objects.get(pk=self.compas),
                               'ISBX0020000586'))
        
        #test loss and damage types. The same story. It's stupid :)
        self.assertEqual(ets.models.LossDamageType.objects.count(), 3)
        
        """test stock update"""
        self.assertEqual(ets.models.StockItem.objects.count(), 3)
        stock_item = ets.models.StockItem.objects.get(pk='testme0124')
        
        #Commodity name and category
        self.assertTupleEqual((stock_item.commodity.name, stock_item.commodity.category.pk), (u'WHEET', u'SED'))
        
        #After import we've got net --> number_of_units and quantity_net == 1
        self.assertTupleEqual((stock_item.number_of_units, stock_item.unit_weight_net), (1000, 1))
        
        #Update changed stock
        ets.models.EpicStock.objects.using(self.compas).filter(origin_id='testme0124').update(quantity_net=700)
        ets.models.EpicStock.update(self.compas)
        
        self.assertEqual(ets.models.StockItem.objects.get(pk='testme0124').number_of_units, 700)
        
        #Deleted stock
        ets.models.EpicStock.objects.using(self.compas).filter(origin_id='testme0124').delete()
        ets.models.EpicStock.update(self.compas)
        
        self.assertEqual(ets.models.StockItem.objects.get(pk='testme0124').number_of_units, 0)
        
        """Update orders"""
        order = ets.models.Order.objects.all()[0]
        self.assertEqual(order.warehouse, wh)
        self.assertEqual(order.location, ets.models.Location.objects.get(pk='ISBX'))
        self.assertEqual(order.consignee, ets.models.Organization.objects.get(pk='DOEAF'))
        
        #Test updated consignee's name
        self.assertEqual(ets.models.Organization.objects.get(pk='DOEAF').name, 'First consignee in our system')
        
        #Test order items
        self.assertEqual(order.items.count(), 1)
        