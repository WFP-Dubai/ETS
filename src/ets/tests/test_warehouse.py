### -*- coding: utf-8 -*- ####################################################
from django.test import TestCase
from django.core.management import call_command

from ets.models import Warehouse, Location, Consignee

class GetWarehouseTestCase(TestCase):
    
    multi_db = True
    fixtures = ('compas.json',)
    
    def test_get_warhouses(self):
        call_command('sync_compas', nodelete=True)
        location = Location.objects.get(pk="OE7X")
        warehouses = Warehouse.get_warehouses(location=location)
        self.assertEqual(warehouses.count(),1)
        #self.assertEqual(warehouses[0].name="EDO OFFICE MEHTI")
        location = Location.objects.get(code="ISBX")
        ogranization = Consignee.objects.get(code="DOEAF")
        warehouses = Warehouse.get_warehouses(location=location, organization=ogranization)
        self.assertEqual(warehouses.count(),2)
    