### -*- coding: utf-8 -*- ####################################################

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import serializers
from django.utils import simplejson

from ..models import Waybill, LoadingDetail, LtiOriginal, EpicStock, DispatchPoint, urllib2

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

class ApiEmptyServerTestCase(TestCase):
    
    fixtures = ()
    
    def setUp(self):
        self.serialized_data = '[{"pk": "OE7X001", "model": "ets.place", "fields": {"name": "EDO OFFICE MEHTI", "reporting_code": "KARX001", "organization_id": "", "geo_point_code": "OE7X", "country_code": "586", "geo_name": "THARPARKAR"}}, {"pk": "ISBX002", "model": "ets.place", "fields": {"name": "PAKISTAN COUNTRY OFFICE", "reporting_code": "HQX0001", "organization_id": "", "geo_point_code": "ISBX", "country_code": "586", "geo_name": "ISLAMABAD_CAP"}}, {"pk": 1, "model": "ets.waybill", "fields": {"waybillNumber": "A0009", "invalidated": false, "transportVehicleRegistration": "", "transportContractor": "HAMAYOON AND CO", "dispatchRemarks": "", "dateOfDispatch": "2011-06-12", "recipientArrivalDate": null, "recipientConsingee": "WORLD FOOD PROGRAMME", "transportSubContractor": "", "transportDeliverySignedTimestamp": null, "recipientDistance": null, "recipientName": "", "containerTwoSealNumber": "", "auditComment": "Print Dispatch Original", "dispatcherSigned": true, "waybillProcessedForPayment": false, "recipientSignedTimestamp": null, "dispatcherTitle": "LOGISTICS OFFICER", "containerOneSealNumber": "", "transportDeliverySigned": false, "containerTwoRemarksReciept": "", "ltiNumber": "QANX0010010128226P", "containerOneRemarksReciept": "", "transportDispachSignedTimestamp": "2011-06-12 13:12:43", "transactionType": "WIT", "status": 1, "containerTwoRemarksDispatch": "", "recipientSigned": false, "transportDispachSigned": true, "dateOfLoading": "2011-06-12", "recipientEndDischargeDate": null, "recipientRemarks": "", "waybillSentToCompas": false, "recipientStartDischargeDate": null, "containerOneRemarksDispatch": "", "slug": "isbx002a0009", "waybillValidated": false, "transportType": "02", "dispatch_warehouse": "ISBX002", "destinationWarehouse": "OE7X001", "recipientLocation": "SUKKHUR", "waybillRecSentToCompas": false, "transportDriverName": "", "dispatcherName": "ISBX0020000586", "transportDriverLicenceID": "", "containerOneNumber": "", "recipientTitle": "", "containerTwoNumber": "", "waybillReceiptValidated": false, "transportTrailerRegistration": ""}}, {"pk": 1, "model": "ets.loadingdetail", "fields": {"numberUnitsGood": "0", "unitsDamagedType": null, "unitsLostReason": null, "numberUnitsLost": "0", "wbNumber": 1, "overloadedUnits": false, "numberUnitsLoaded": "5", "order_item": 1, "unitsDamagedReason": null, "unitsLostType": null, "loadingDetailSentToCompas": false, "overOffloadUnits": false, "numberUnitsDamaged": "0"}}, {"pk": 2, "model": "ets.loadingdetail", "fields": {"numberUnitsGood": "0", "unitsDamagedType": null, "unitsLostReason": null, "numberUnitsLost": "0", "wbNumber": 1, "overloadedUnits": false, "numberUnitsLoaded": "10", "order_item": 1, "unitsDamagedReason": null, "unitsLostType": null, "loadingDetailSentToCompas": false, "overOffloadUnits": false, "numberUnitsDamaged": "0"}}]'
    
    def create_objects(self):
        for obj in serializers.deserialize('json', self.serialized_data):
            obj.save()
    
    def test_send_new(self):
        
        self.assertEqual(Waybill.objects.count(), 0)
        
        response = self.client.post(reverse("api_new_waybill"), data=self.serialized_data, content_type="application/json")
        self.assertEqual(response.content, "Created")
        
        self.assertEqual(Waybill.objects.count(), 1)
        self.assertEqual(Waybill.objects.get(pk=1).loading_details.count(), 2)
    
    def test_get_informed(self):
        #Create objects
        self.create_objects()
        #Change status of first one
        Waybill.objects.filter(pk=1).update(status=Waybill.INFORMED)
        
        response = self.client.get(reverse("api_informed_waybill", kwargs={"id": 1}))
        self.assertContains(response, '"pk": 1', status_code=200)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
    
    def test_get_delivered(self):
        #Create objects
        self.create_objects()
        #Change status of first one
        Waybill.objects.filter(pk=1).update(status=Waybill.DELIVERED)
        original = Waybill.objects.get(pk=1)
        
        response = self.client.get(reverse("api_delivered_waybill", kwargs={"id": 1}))
        self.assertEqual(response["Content-Type"], "text/xml; charset=utf-8")
        
        waybill = serializers.deserialize('xml', response.content).next().object
        self.assertEqual(waybill, original)
        
        
class ApiClientTestCase(ApiServerTestCase):
        
    def test_send_new(self):
        
        #MonkeyPatch of urlopen
        def dummy_urlopen(request, timeout):
            
            class DummyResponse(object):
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
                    return """<?xml version="1.0" encoding="utf-8"?>
<django-objects version="1.0">
 <object pk="1" model="ets.waybill">
  <field type="IntegerField" name="status">4</field>
  <field type="SlugField" name="slug">isbx002a0009</field>
  <field type="CharField" name="ltiNumber">QANX0010010128226P</field>
  <field type="CharField" name="waybillNumber">A0009</field>
  <field type="DateField" name="dateOfLoading">2011-06-12</field>
  <field type="DateField" name="dateOfDispatch">2011-06-12</field>
  <field type="CharField" name="transactionType">WIT</field>
  <field type="CharField" name="transportType">02</field>
  <field type="CharField" name="dispatchRemarks"></field>
  <field type="TextField" name="dispatcherName">ISBX0020000586</field>
  <field type="TextField" name="dispatcherTitle">LOGISTICS OFFICER</field>
  <field type="BooleanField" name="dispatcherSigned">True</field>
  <field to="ets.place" name="dispatch_warehouse" rel="ManyToOneRel">ISBX002</field>
  <field type="TextField" name="transportContractor">HAMAYOON AND CO</field>
  <field type="TextField" name="transportSubContractor"></field>
  <field type="TextField" name="transportDriverName"></field>
  <field type="TextField" name="transportDriverLicenceID"></field>
  <field type="TextField" name="transportVehicleRegistration"></field>
  <field type="TextField" name="transportTrailerRegistration"></field>
  <field type="BooleanField" name="transportDispachSigned">True</field>
  <field type="DateTimeField" name="transportDispachSignedTimestamp">2011-06-12 13:12:43</field>
  <field type="BooleanField" name="transportDeliverySigned">False</field>
  <field type="DateTimeField" name="transportDeliverySignedTimestamp"><None></None></field>
  <field type="CharField" name="containerOneNumber"></field>
  <field type="CharField" name="containerTwoNumber"></field>
  <field type="CharField" name="containerOneSealNumber"></field>
  <field type="CharField" name="containerTwoSealNumber"></field>
  <field type="CharField" name="containerOneRemarksDispatch"></field>
  <field type="CharField" name="containerTwoRemarksDispatch"></field>
  <field type="CharField" name="containerOneRemarksReciept"></field>
  <field type="CharField" name="containerTwoRemarksReciept"></field>
  <field type="CharField" name="recipientLocation">SUKKHUR</field>
  <field type="CharField" name="recipientConsingee">WORLD FOOD PROGRAMME</field>
  <field type="CharField" name="recipientName"></field>
  <field type="CharField" name="recipientTitle"></field>
  <field type="DateField" name="recipientArrivalDate"><None></None></field>
  <field type="DateField" name="recipientStartDischargeDate"><None></None></field>
  <field type="DateField" name="recipientEndDischargeDate"><None></None></field>
  <field type="IntegerField" name="recipientDistance"><None></None></field>
  <field type="TextField" name="recipientRemarks"></field>
  <field type="BooleanField" name="recipientSigned">False</field>
  <field type="DateTimeField" name="recipientSignedTimestamp"><None></None></field>
  <field to="ets.place" name="destinationWarehouse" rel="ManyToOneRel">OE7X001</field>
  <field type="BooleanField" name="waybillValidated">False</field>
  <field type="BooleanField" name="waybillReceiptValidated">False</field>
  <field type="BooleanField" name="waybillSentToCompas">False</field>
  <field type="BooleanField" name="waybillRecSentToCompas">False</field>
  <field type="BooleanField" name="waybillProcessedForPayment">False</field>
  <field type="BooleanField" name="invalidated">False</field>
  <field type="TextField" name="auditComment">Print Dispatch Original</field>
 </object>
</django-objects>
"""
            
            return DummyResponse()
        
        urllib2.urlopen = dummy_urlopen
        
        self.waybill.update_status(Waybill.INFORMED)
        
        Waybill.get_delivered()
        self.assertEqual(Waybill.objects.get(pk=1).status, Waybill.DELIVERED)


    #===================================================================================================================
    # 
    # def test_waybill_reception(self):
    #    """ets.views.waybill_reception test"""
    #    response = self.client.get(reverse("waybill_reception", args=(self.waybill.pk,)))
    #    self.assertEqual(response.status_code, 200)
    #    
    #    self.assertTrue(isinstance(response.context["form"], WaybillRecieptForm))
    #    self.assertEqual(response.context["form"].instance, self.waybill)
    #    #TODO: Append more tests for this view and form inside it.
    # 
    # def test_waybill_search(self):
    #    """ets.views.waybill_search test"""
    #    response = self.client.get(reverse("waybill_search"))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTupleEqual(tuple(response.context["waybill_list"]), (self.waybill,))
    #    self.assertTupleEqual(tuple(response.context["my_wb"]), (self.waybill.pk,))
    #    
    # def test_create_waybill(self):
    #    """ets.views.waybillCreate test"""
    #    response = self.client.get(reverse("waybillCreate", args=(self.lti.code,)))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTrue(self.lti in response.context["lti_list"])
    #    self.assertTrue(isinstance(response.context["form"], WaybillForm))
    #    self.assertEqual(response.context["form"].initial, {
    #        "dateOfDispatch": datetime.date.today(),
    #        "dateOfLoading": datetime.date.today(),
    #        "destinationWarehouse": "",
    #        "dispatcherName": u"ISBX0020000586",
    #        "dispatcherTitle": u"LOGISTICS OFFICER",
    #        "invalidated": "False",
    #        "ltiNumber": u"QANX0010010128226P",
    #        "recipientConsingee": u"DEPARTMENT OF EDUCATION AFGHANISTAN",
    #        "recipientLocation": u"QANDAHAR CITY",
    #        "transportContractor": u" MUSLIM TRANSPORT",
    #        "waybillNumber": "N/A"
    #    })
    # 
    #===================================================================================================================