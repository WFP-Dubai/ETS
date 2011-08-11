### -*- coding: utf-8 -*- ####################################################
import os
import urllib2

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import simplejson
from django.core.management import call_command

#from ..models import Waybill, LoadingDetail, LtiOriginal, EpicStock, DispatchPoint, LtiWithStock, urllib2
import ets.models
from ..models import Waybill, LtiOriginal, EpicStock, Warehouse, Waybill
from ets.utils import update_compas
from ets.api.client import *
import ets.api.client

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
        return Waybill.objects.get(pk="ISBX00211A")
    

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
    
    def test_get_receiving(self):
        #Change status of first one
        self.get_waybill().update_status(status=Waybill.SENT)
        
        response = self.client.get(reverse("api_receiving_waybill", 
                                           kwargs={"destination": self.get_waybill().destination.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        
        #Check iterator and existence of waybill in result
        self.assertTrue(self.get_waybill() in (obj.object for obj in serializers.deserialize('json', response.content)))
    
    def test_get_delivered(self):
        #Change status of first one
        self.get_waybill().update_status(status=Waybill.DELIVERED)
        
        response = self.client.get(reverse("api_delivered_waybill", kwargs={"slug": self.get_waybill().pk}))
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        
        waybill = serializers.deserialize('json', response.content).next().object
        self.assertEqual(waybill, self.get_waybill())
    
    
class ApiEmptyServerTestCase(TestCase):
    
    fixtures = ()
    
    def create_objects(self):
        call_command('loaddata', 'development.json', **{
            'verbosity': 0,
            'commit': False,
            #'database': db
        })
        #===============================================================================================================
        # for obj in serializers.deserialize('json', self.serialized_data):
        #    obj.save()
        #===============================================================================================================
    
    def get_waybill(self):
        return Waybill.objects.all()[0]
    
    def test_send_new(self):
       
        self.assertEqual(Waybill.objects.count(), 0)
        
        serialized_data = get_fixture_text('development.json')

        response = self.client.post(reverse("api_new_waybill"), data=serialized_data, content_type="application/json")
        self.assertEqual(response.content, "Created")
        
        self.assertEqual(Waybill.objects.count(), 1)
        self.assertEqual(self.get_waybill().loading_details.count(), 1)
        self.assertEqual(self.get_waybill().status, Waybill.SENT)
    
    def test_get_receiving(self):
        
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 200
                
                #=======================================================================================================
                # def __getitem__(self, name):
                #    if name == 'Content-Type':
                #        return "application/json; charset=utf-8"
                #    else:
                #        raise AttributeError("There is no item with name %s" % name)
                #=======================================================================================================
                
                def read(self):
                    return get_fixture_text('development.json')
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.assertEqual(Waybill.objects.count(), 0)
        get_receiving()
        
        self.assertEqual(Waybill.objects.count(), 1)
        self.assertEqual(self.get_waybill().loading_details.count(), 1)
        #self.assertEqual(self.get_waybill().status, Waybill.SENT)
    
    def test_get_informed(self):
        #Create objects
        self.create_objects()
        #Change status of first one
        waybill = self.get_waybill()
        waybill.update_status(status=Waybill.INFORMED)
        
        response = self.client.get(reverse("api_informed_waybill", kwargs={"slug": waybill.slug}))
        self.assertContains(response, '"pk": "ISBX00211A"', status_code=200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
    
    def test_update_informed(self):
        #Create objects
        self.create_objects()
        
        self.get_waybill().update_status(Waybill.SENT)
        
        #Bad request
        response = self.client.put(reverse("api_informed_waybill"))
        self.assertEqual(response.status_code, 400)
        
        #Provide content-type
        response = self.client.put(reverse("api_informed_waybill"), data='["ISBX00211A"]', content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(self.get_waybill().status, Waybill.INFORMED)
    
    def test_send_delivered(self):
        #Create objects
        self.create_objects()
        
        self.assertNotEqual(self.get_waybill().status, Waybill.DELIVERED)
        
        #Provide content-type
        response = self.client.put(reverse("api_delivered_waybill"), 
                                   data=get_fixture_text('test_delivered_sync.json'), 
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(self.get_waybill().status, Waybill.DELIVERED)
        
        
class ApiClientTestCase(TestDevelopmentMixin, TestCase):
        
    def test_send_new(self):
        
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 201
                def read(self):
                    return "Created"
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.get_waybill().update_status(Waybill.SIGNED)
        send_new()
        self.assertEqual(self.get_waybill().status, Waybill.SENT)
        
    def test_get_informed(self):
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 200
                
                def read(self):
                    return '{"pk": 1}'
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.get_waybill().update_status(Waybill.SENT)
        
        get_informed()
        self.assertEqual(self.get_waybill().status, Waybill.INFORMED)
    
    def test_update_informed(self):
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 200
                
                def read(self):
                    return "OK"
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        old_compas = ets.api.client.COMPAS_STATION
        ets.api.client.COMPAS_STATION = "ISBX003"
        
        self.get_waybill().update_status(Waybill.SENT)
        send_informed()
        self.assertEqual(self.get_waybill().status, Waybill.INFORMED)
        
        ets.api.client.COMPAS_STATION = old_compas
    
    def test_get_delivered(self):
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 200
                
                #=======================================================================================================
                # def __getitem__(self, name):
                #    if name == 'Content-Type':
                #        return "application/json; charset=utf-8"
                #    else:
                #        raise AttributeError("There is no item with name %s" % name)
                #=======================================================================================================
                
                def read(self):
                    return get_fixture_text('test_delivered_sync.json')
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.get_waybill().update_status(Waybill.INFORMED)
        
        get_delivered()
        self.assertEqual(self.get_waybill().status, Waybill.DELIVERED)
    
    def test_update_delivered(self):
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 200
                
                def read(self):
                    return "OK"
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        old_compas = ets.api.client.COMPAS_STATION
        ets.api.client.COMPAS_STATION = "ISBX003"
        
        self.get_waybill().update_status(Waybill.DELIVERED)
        send_delivered()
        self.assertEqual(self.get_waybill().status, Waybill.COMPLETE)
        
        ets.api.client.COMPAS_STATION = old_compas
