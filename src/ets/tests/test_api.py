### -*- coding: utf-8 -*- ####################################################
import os

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import simplejson
from django.core.management import call_command

from ..models import Waybill, LoadingDetail, LtiOriginal, EpicStock, DispatchPoint, LtiWithStock, urllib2
import ets.models

class ApiServerTestCase(TestCase):
    
    #multi_db = True
    fixtures = ["development.json", ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.client.login(username="admin", password="admin")
        self.user = User.objects.get(username="admin")
        self.waybill = Waybill.objects.get(pk=1)
        self.lti = LtiOriginal.objects.get(pk="QANX001000000000000005217HQX0001000000000000984141")
        self.stock = EpicStock.objects.get(pk="KARX025KARX0010000944801MIXMIXHEBCG15586")
        self.dispatch_point = DispatchPoint.objects.get(pk=1)
        self.maxDiff = None
        self.waybill_dict = {
            'slug': 'isbx002a0009',
            'status': 1,
            'dispatch_warehouse': {
                'country_code': '586',
                'geo_name': 'ISLAMABAD_CAP',
                'geo_point_code': 'ISBX',
                'name': 'PAKISTAN COUNTRY OFFICE',
                'org_code': 'ISBX002',
                'reporting_code': 'HQX0001'},
            "waybillNumber": "A0009",
            "transportVehicleRegistration": "",
            "transportContractor": "HAMAYOON AND CO",
            "dispatchRemarks": "",
            "dateOfDispatch": "2011-06-12",
            "recipientArrivalDate": None,
            "recipientConsingee": "WORLD FOOD PROGRAMME",
            "transportSubContractor": "",
            "transportDeliverySignedTimestamp": None,
            "recipientDistance": None,
            "recipientName": "",
            "auditComment": "Print Dispatch Original",
            "dispatcherSigned": True,
            "waybillProcessedForPayment": False,
            "recipientSignedTimestamp": None,
            "dispatcherTitle": "LOGISTICS OFFICER",
            "containerTwoSealNumber": "",
            "transportDeliverySigned": False,
            "containerTwoRemarksReciept": "",
            "ltiNumber": "QANX0010010128226P",
            "containerOneRemarksReciept": "",
            "transportDispachSignedTimestamp": "2011-06-12 13:12:43",
            "transactionType": "WIT",
            "invalidated": False,
            "containerTwoRemarksDispatch": "",
            "recipientSigned": False,
            "transportDispachSigned": True,
            "dateOfLoading": "2011-06-12",
            "recipientEndDischargeDate": None,
            "recipientRemarks": "",
            "waybillSentToCompas": False,
            "recipientStartDischargeDate": None,
            "containerOneRemarksDispatch": "",
            "containerOneSealNumber": "",
            "waybillValidated": False,
            "transportType": "02",
            "destinationWarehouse": {
                "name": "EDO OFFICE MEHTI",
                "org_code": "OE7X001",
                "reporting_code": "KARX001",
                #"organization_id": "",
                "geo_point_code": "OE7X",
                "country_code": "586",
                "geo_name": "THARPARKAR"
            },
            "recipientLocation": "SUKKHUR",
            "waybillRecSentToCompas": False,
            "transportDriverName": "",
            "dispatcherName": "ISBX0020000586",
            "transportDriverLicenceID": "",
            "containerOneNumber": "",
            "recipientTitle": "",
            "containerTwoNumber": "",
            "waybillReceiptValidated": False,
            "transportTrailerRegistration": ""
        }
     
    #===================================================================================================================
    # def tearDown(self):
    #    "Hook method for deconstructing the test fixture after testing it."
    #===================================================================================================================
    
    def test_read_waybills(self):
        response = self.client.get(reverse("api_waybill"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        
        data = simplejson.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertDictEqual(data[0], self.waybill_dict)
    
    def test_read_waybill(self):
        response = self.client.get(reverse("api_waybill", kwargs={"id": self.waybill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        
        data = simplejson.loads(response.content)
        self.assertTrue(isinstance(data, dict))
        self.assertDictEqual(data, self.waybill_dict)
    
    def test_get_receiving(self):
        #Change status of first one
        Waybill.objects.filter(pk=1).update(status=Waybill.SENT)
        
        response = self.client.get(reverse("api_receiving_waybill", 
                                           kwargs={"destination": self.waybill.destinationWarehouse.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        
        #Check iterator and existence of waybill in result
        self.assertTrue(self.waybill in (obj.object for obj in serializers.deserialize('json', response.content)))
    
    def test_get_delivered(self):
        #Change status of first one
        Waybill.objects.filter(pk=1).update(status=Waybill.DELIVERED)
        
        response = self.client.get(reverse("api_delivered_waybill", kwargs={"id": 1}))
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        
        waybill = serializers.deserialize('json', response.content).next().object
        self.assertEqual(waybill, self.waybill)
    
    
class ApiEmptyServerTestCase(TestCase):
    
    fixtures = ()
    
    def create_objects(self):
        call_command('loaddata', 'test_sync.json', **{
            'verbosity': 0,
            'commit': False,
            #'database': db
        })
        #===============================================================================================================
        # for obj in serializers.deserialize('json', self.serialized_data):
        #    obj.save()
        #===============================================================================================================
    
    def test_send_new(self):
        
        self.assertEqual(Waybill.objects.count(), 0)
        
        serialized_data = open(os.path.join(os.path.dirname(__file__), '../fixtures/test_sync.json')).read()

        response = self.client.post(reverse("api_new_waybill"), data=serialized_data, content_type="application/json")
        self.assertEqual(response.content, "Created")
        
        self.assertEqual(Waybill.objects.count(), 1)
        self.assertEqual(Waybill.objects.get(pk=1).loading_details.count(), 2)
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.SENT)
    
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
                    return open(os.path.join(os.path.dirname(__file__), '../fixtures/test_sync.json')).read()
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        #self.waybill.update_status(Waybill.INFORMED)
        
        self.assertEqual(Waybill.objects.count(), 0)
        Waybill.get_receiving()
        
        self.assertEqual(Waybill.objects.count(), 1)
        self.assertEqual(Waybill.objects.get(pk=1).loading_details.count(), 2)
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.SENT)
    
    def test_get_informed(self):
        #Create objects
        self.create_objects()
        #Change status of first one
        Waybill.objects.filter(pk=1).update(status=Waybill.INFORMED)
        
        response = self.client.get(reverse("api_informed_waybill", kwargs={"id": 1}))
        self.assertContains(response, '"pk": 1', status_code=200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
    
    def test_update_informed(self):
        #Create objects
        self.create_objects()
        
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.SENT)
        
        #Bad request
        response = self.client.put(reverse("api_informed_waybill"))
        self.assertEqual(response.status_code, 400)
        
        #Provide content-type
        response = self.client.put(reverse("api_informed_waybill"), data='[1]', content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.INFORMED)
        
class ApiClientTestCase(ApiServerTestCase):
        
    def test_send_new(self):
        
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 201
                def read(self):
                    return "Created"
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.NEW)
        Waybill.send_new()
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.SENT)
        
    def test_get_informed(self):
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 200
                
                def read(self):
                    return '{"pk": 1}'
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.waybill.update_status(Waybill.SENT)
        
        Waybill.get_informed()
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.INFORMED)
    
    def test_update_informed(self):
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
                code = 200
                
                def read(self):
                    return "OK"
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        old_compas = ets.models.COMPAS_STATION
        ets.models.COMPAS_STATION = "OE7X001"
        
        Waybill.objects.filter(pk=1).update(status=Waybill.SENT)
        Waybill.send_informed()
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.INFORMED)
        
        ets.models.COMPAS_STATION = old_compas
    
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
                    return """[
 {
  "pk": 1,
  "model": "ets.waybill",
  "fields": {
   "waybillNumber": "A0009",
   "invalidated": false,
   "transportVehicleRegistration": "",
   "transportContractor": "HAMAYOON AND CO",
   "dispatchRemarks": "",
   "dateOfDispatch": "2011-06-12",
   "recipientArrivalDate": null,
   "recipientConsingee": "WORLD FOOD PROGRAMME",
   "transportSubContractor": "",
   "transportDeliverySignedTimestamp": null,
   "recipientDistance": null,
   "recipientName": "",
   "containerTwoSealNumber": "",
   "auditComment": "Print Dispatch Original",
   "dispatcherSigned": true,
   "waybillProcessedForPayment": false,
   "recipientSignedTimestamp": null,
   "dispatcherTitle": "LOGISTICS OFFICER",
   "containerOneSealNumber": "",
   "transportDeliverySigned": false,
   "containerTwoRemarksReciept": "",
   "ltiNumber": "QANX0010010128226P",
   "containerOneRemarksReciept": "",
   "transportDispachSignedTimestamp": "2011-06-12 13:12:43",
   "transactionType": "WIT",
   "status": 4,
   "containerTwoRemarksDispatch": "",
   "recipientSigned": false,
   "transportDispachSigned": true,
   "dateOfLoading": "2011-06-12",
   "recipientEndDischargeDate": null,
   "recipientRemarks": "",
   "waybillSentToCompas": false,
   "recipientStartDischargeDate": null,
   "containerOneRemarksDispatch": "",
   "slug": "isbx002a0009",
   "waybillValidated": false,
   "transportType": "02",
   "dispatch_warehouse": "ISBX002",
   "destinationWarehouse": "OE7X001",
   "recipientLocation": "SUKKHUR",
   "waybillRecSentToCompas": false,
   "transportDriverName": "",
   "dispatcherName": "ISBX0020000586",
   "transportDriverLicenceID": "",
   "containerOneNumber": "",
   "recipientTitle": "",
   "containerTwoNumber": "",
   "waybillReceiptValidated": false,
   "transportTrailerRegistration": ""
  }
 }
]
"""
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.waybill.update_status(Waybill.INFORMED)
        
        Waybill.get_delivered()
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.DELIVERED)
