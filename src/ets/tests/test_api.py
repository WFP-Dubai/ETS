### -*- coding: utf-8 -*- ####################################################
import os
import urllib2
import csv
import StringIO

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import simplejson
from django.core.management import call_command

#from ..models import Waybill, LoadingDetail, LtiOriginal, EpicStock, DispatchPoint, LtiWithStock, urllib2
import ets.models
#from ..models import Waybill, LtiOriginal, EpicStock, Warehouse,
from ets.utils import update_compas

def get_fixture_text(file_name):
    return open(os.path.join(os.path.dirname(__file__), '../fixtures', file_name)).read()

class TestDevelopmentMixin(object):

    multi_db = True
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."        
        call_command('loaddata', 'compas.json', verbosity=0, commit=False, database='compas')
        update_compas()
        call_command('loaddata', 'development.json', verbosity=0, commit=False, database='default')

        self.client.login(username="admin", password="admin")
        self.user = User.objects.get(username="admin")
        #self.lti = LtiOriginal.objects.get(pk="QANX001000000000000005217HQX0001000000000000984141")
        #self.stock = EpicStock.objects.get(pk="KARX025KARX0010000944801MIXMIXHEBCG15586")
        #self.dispatch_point = Warehouse.objects.get(pk=1)
        self.maxDiff = None
    
    def get_waybill(self):
        return ets.models.Waybill.objects.get(pk="ISBX00211A")
    

class ApiServerTestCase(TestDevelopmentMixin, TestCase):
    
    #===========================================================================
    # def test_read_waybills(self):
    #    response = self.client.get(reverse("api_waybill"))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
    #    
    #    data = simplejson.loads(response.content)
    #    self.assertTrue(isinstance(data, list))
    #    self.assertDictEqual(data[0], self.waybill_dict)
    #===========================================================================
    
    #===========================================================================
    # def test_read_waybill(self):
    #    response = self.client.get(reverse("api_waybill", kwargs={"slug": self.get_waybill().pk}))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
    #    
    #    data = simplejson.loads(response.content)
    #    self.assertTrue(isinstance(data, dict))
    #    self.assertDictEqual(data, self.waybill_dict)
    #===========================================================================
    
    
        
    def test_get_waybills(self):

        # All waybills
        response = self.client.get(reverse("api_waybills"))
        self.assertEqual(response["Content-Type"], "application/csv")
        self.assertContains(response, 'ISBX00211A', status_code=200)
        # One wabill
        response = self.client.get(reverse("api_waybills", kwargs={"slug": self.get_waybill().slug}))
        self.assertContains(response, 'ISBX00211A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result)
        item = dict_reader.next()
        self.assertEqual(item['slug'], self.get_waybill().slug)
        # Waybills with destination and warehouse
        response = self.client.get(reverse("api_waybills", kwargs={"warehouse": self.get_waybill().warehouse.code, 
                                                                   "destination": self.get_waybill().destination.code}))
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'ISBX003', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        
        
    def test_get_loading_details(self):

        # All Loading details
        response = self.client.get(reverse("api_loading_details"))
        self.assertContains(response, 'ISBX00211A1', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        # Loading details for one waybill
        response = self.client.get(reverse("api_loading_details", kwargs={"waybill": self.get_waybill().slug}))
        self.assertContains(response, 'ISBX00211A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result)
        item = dict_reader.next()
        self.assertEqual(item['order code'], self.get_waybill().order_code)
        # Loading details for some destination and some warehouse
        response = self.client.get(reverse("api_loading_details", kwargs={"warehouse": self.get_waybill().warehouse.code, 
                                                                    "destination": self.get_waybill().destination.code}))
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'ISBX003', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        
    def test_get_orders(self):

        order = ets.models.Order.objects.get(pk='OURLITORDER')
        # All orders
        response = self.client.get(reverse("api_orders"))
        self.assertContains(response, 'OURLITORDER', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        # One order
        response = self.client.get(reverse("api_orders", kwargs={"code": order.code}))
        self.assertContains(response, 'OURLITORDER', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result)
        item = dict_reader.next()
        self.assertEqual(item['Code'], order.code)
        # Orders with destination and warehouse
        response = self.client.get(reverse("api_orders", kwargs={"warehouse": order.warehouse.code, 
                                                        "destination": order.consignee.warehouses.all()[0].code}))
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'DOEAF', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        
        
    def test_get_order_items(self):

        order = ets.models.Order.objects.get(pk='OURLITORDER')
        # All order items
        response = self.client.get(reverse("api_order_items"))
        self.assertContains(response, 'OURLITORDER', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        # Order items for one order
        response = self.client.get(reverse("api_order_items", kwargs={"order": order.code}))
        self.assertContains(response, 'OURLITORDER', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result)
        item = dict_reader.next()
        self.assertEqual(item['Code'], order.code)
        # Order items for some destination and some warehouse
        response = self.client.get(reverse("api_order_items", kwargs={"warehouse": order.warehouse.code, 
                                                        "destination": order.consignee.warehouses.all()[0].code}))
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'DOEAF', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        
    def test_get_stock_items(self):
        
        warehouse = ets.models.Warehouse.objects.get(pk='ISBX002')
        # All stock items
        response = self.client.get(reverse("api_stock_items"))
        self.assertContains(response, warehouse.code, status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        # Stock items for one warehouse
        response = self.client.get(reverse("api_stock_items", kwargs={"warehouse": warehouse.code}))
        self.assertContains(response, warehouse.code, status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result)
        item = dict_reader.next()
        self.assertEqual(item['Warehouse'], warehouse.code)
        