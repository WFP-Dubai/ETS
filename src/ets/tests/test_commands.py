### -*- coding: utf-8 -*- ####################################################

from django.test import TestCase
from django.core.management import call_command

import ets.models

class CommandTestCase(TestCase):
    
    multi_db = True
    fixtures = ('compas.json',)
    
    def test_sync_compas(self):
        
        self.assertEqual(ets.models.Place.objects.using('compas').count(), 3)
        self.assertEqual(ets.models.Location.objects.count(), 0)
        self.assertEqual(ets.models.Warehouse.objects.count(), 0)
        self.assertEqual(ets.models.Consignee.objects.count(), 0)
        
        call_command('sync_compas', nodelete=True)
        
        """Test place's update method"""
        self.assertEqual(ets.models.Location.objects.count(), 2)
        self.assertEqual(ets.models.Warehouse.objects.count(), 3)
        self.assertEqual(ets.models.Consignee.objects.count(), 1)
        
        warehouse = ets.models.Warehouse.objects.get(pk='ISBX002')
        self.assertTupleEqual((warehouse.organization, warehouse.location) , 
                              (ets.models.Consignee.objects.get(pk='DOEAF'), 
                               ets.models.Location.objects.get(pk='ISBX')))
        
        #test compas persons. It's silly, because test case've already created such persons
        self.assertEqual(ets.models.CompasPerson.objects.count(), 2)
        
        #test loss and damage types. The same story. It's stupid :)
        self.assertEqual(ets.models.LossDamageType.objects.count(), 3)
        
        """test stock update"""
        self.assertEqual(ets.models.StockItem.objects.count(), 2)
        stock_item = ets.models.StockItem.objects.get(pk='testme0124')
        
        #After import we've got net --> number_of_units and quantity_net == 1
        self.assertTupleEqual((stock_item.number_of_units, stock_item.unit_weight_net), (1000, 1))
        
        #Update changed stock
        ets.models.EpicStock.objects.using('compas').filter(origin_id='testme0124').update(quantity_net=700)
        ets.models.EpicStock.update()
        
        self.assertEqual(ets.models.StockItem.objects.get(pk='testme0124').number_of_units, 700)
        
        #Deleted stock
        ets.models.EpicStock.objects.using('compas').filter(origin_id='testme0124').delete()
        ets.models.EpicStock.update()
        
        self.assertEqual(ets.models.StockItem.objects.get(pk='testme0124').number_of_units, 0)
        
        """Update orders"""
        order = ets.models.Order.objects.all()[0]
        self.assertEqual(order.warehouse, warehouse)
        self.assertEqual(order.location, ets.models.Location.objects.get(pk='ISBX'))
        self.assertEqual(order.consignee, ets.models.Consignee.objects.get(pk='DOEAF'))
        
        #Test updated consignee's name
        self.assertEqual(ets.models.Consignee.objects.get(pk='DOEAF').name, 'First consignee in our system')
        
        #Test order items
        self.assertEqual(order.items.count(), 1)
        