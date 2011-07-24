### -*- coding: utf-8 -*- ####################################################

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import simplejson
from django.contrib.auth.models import User

from ..models import Waybill, LtiOriginal, EpicStock, DispatchPoint

class ApiTestCase(TestCase):
    
    #multi_db = True
    fixtures = ['development.json', ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.client.login(username='admin', password='admin')
        self.user = User.objects.get(username="admin")
        self.waybill = Waybill.objects.get(pk=1)
        self.lti = LtiOriginal.objects.get(pk="QANX001000000000000005217HQX0001000000000000984141")
        self.stock = EpicStock.objects.get(pk="KARX025KARX0010000944801MIXMIXHEBCG15586")
        self.dispatch_point = DispatchPoint.objects.get(pk=1)
        self.maxDiff = None
        self.waybill_dict = {
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
                #'organization_id': '',
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
    
    def test_waybill_list(self):
        response = self.client.get(reverse('api_waybill'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/json; charset=utf-8")
        
        data = simplejson.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertDictEqual(data[0], self.waybill_dict)
    
    def test_one_waybill(self):
        response = self.client.get(reverse('api_waybill', kwargs={'waybill_pk': self.waybill.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/json; charset=utf-8")
        
        data = simplejson.loads(response.content)
        self.assertTrue(isinstance(data, dict))
        self.assertDictEqual(data, self.waybill_dict)
        
        
        

        
    #===================================================================================================================
    # 
    # def test_waybill_reception(self):
    #    """ets.views.waybill_reception test"""
    #    response = self.client.get(reverse('waybill_reception', args=(self.waybill.pk,)))
    #    self.assertEqual(response.status_code, 200)
    #    
    #    self.assertTrue(isinstance(response.context['form'], WaybillRecieptForm))
    #    self.assertEqual(response.context['form'].instance, self.waybill)
    #    #TODO: Append more tests for this view and form inside it.
    # 
    # def test_waybill_search(self):
    #    """ets.views.waybill_search test"""
    #    response = self.client.get(reverse('waybill_search'))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTupleEqual(tuple(response.context['waybill_list']), (self.waybill,))
    #    self.assertTupleEqual(tuple(response.context['my_wb']), (self.waybill.pk,))
    #    
    # def test_create_waybill(self):
    #    """ets.views.waybillCreate test"""
    #    response = self.client.get(reverse('waybillCreate', args=(self.lti.code,)))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTrue(self.lti in response.context['lti_list'])
    #    self.assertTrue(isinstance(response.context['form'], WaybillForm))
    #    self.assertEqual(response.context['form'].initial, {
    #        'dateOfDispatch': datetime.date.today(),
    #        'dateOfLoading': datetime.date.today(),
    #        'destinationWarehouse': '',
    #        'dispatcherName': u'ISBX0020000586',
    #        'dispatcherTitle': u'LOGISTICS OFFICER',
    #        'invalidated': 'False',
    #        'ltiNumber': u'QANX0010010128226P',
    #        'recipientConsingee': u'DEPARTMENT OF EDUCATION AFGHANISTAN',
    #        'recipientLocation': u'QANDAHAR CITY',
    #        'transportContractor': u' MUSLIM TRANSPORT',
    #        'waybillNumber': 'N/A'
    #    })
    # 
    #===================================================================================================================