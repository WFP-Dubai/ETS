### -*- coding: utf-8 -*- ####################################################

import datetime

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

from ..models import Waybill, LtiOriginal
from ..forms import WaybillRecieptForm, WaybillForm

class UnathenticatedTestCase(TestCase):
    
    #multi_db = True
    fixtures = ['development.json', ]
    
    def test_login_form(self):
        #Check login
        response = self.client.get(reverse('select_action'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('select_action'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], AuthenticationForm))


class WaybillTestCase(TestCase):
    
    fixtures = ['development.json', ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.waybill = Waybill.objects.get(pk=1)
    
    def test_serialize(self):
        """Checks methods serialize of waybill instance"""
        data = self.waybill.serialize()
        self.assertTrue(data.startswith('[{"pk": 1, "model": "ets.waybill", "fields": {"waybillNumber": "A0009",'))
    
    def test_compress(self):
        """Checks methods compress of waybill instance"""
        data = self.waybill.compress()
        self.assertTrue(data.startswith('eJztWG1zokgQ/iuUn7MpQI1mv6GgUlFxgWySulxRExh1LgjuMG4udbX//RpmhAExuW9XV2fKygvd0zz99NM9M+n89tdzZ//63PmqaFfKc2eXRjj'))


class ClientWaybillTestCase(TestCase):
    
    #multi_db = True
    fixtures = ['development.json', ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.client.login(username='admin', password='admin')
        self.user = User.objects.get(username="admin")
        self.waybill = Waybill.objects.get(pk=1)
        self.lti = LtiOriginal.objects.get(pk="QANX001000000000000005217HQX0001000000000000984141")
     
    #===================================================================================================================
    # def tearDown(self):
    #    "Hook method for deconstructing the test fixture after testing it."
    #===================================================================================================================
    
    def test_index(self):
        response = self.client.get(reverse('select_action'))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_reception(self):
        """ets.views.waybill_reception test"""
        response = self.client.get(reverse('waybill_reception', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(isinstance(response.context['form'], WaybillRecieptForm))
        self.assertEqual(response.context['form'].instance, self.waybill)
        #TODO: Append more tests for this view and form inside it.
    
    def test_waybill_search(self):
        """ets.views.waybill_search test"""
        response = self.client.get(reverse('waybill_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTupleEqual(tuple(response.context['waybill_list']), (self.waybill,))
        self.assertTupleEqual(tuple(response.context['my_wb']), (self.waybill.pk,))
        
    def test_create_waybill(self):
        """ets.views.waybillCreate test"""
        response = self.client.get(reverse('waybillCreate', args=(self.lti.code,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.lti in response.context['lti_list'])
        self.assertTrue(isinstance(response.context['form'], WaybillForm))
        self.assertEqual(response.context['form'].initial, {
            'dateOfDispatch': datetime.date.today(),
            'dateOfLoading': datetime.date.today(),
            'destinationWarehouse': '',
            'dispatcherName': u'ISBX0020000586',
            'dispatcherTitle': u'LOGISTICS OFFICER',
            'invalidated': 'False',
            'ltiNumber': u'QANX0010010128226P',
            'recipientConsingee': u'DEPARTMENT OF EDUCATION AFGHANISTAN',
            'recipientLocation': u'QANDAHAR CITY',
            'transportContractor': u' MUSLIM TRANSPORT',
            'waybillNumber': 'N/A'
        })
    
    def test_waybill_view(self):
        """ets.views.waybill_view test"""
        response = self.client.get(reverse('waybill_view', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_validate_form_update(self):
        """ets.views.waybill_validate_form_update test"""
        response = self.client.get(reverse('waybill_validate_form_update', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.lti in response.context['lti_list'])
    
#=======================================================================================================================
#    
#        c = Client()
#        response = c.get(reverse('calendar'))
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, 'для Thornhill')
# 
#    def test_calendar_with_radius(self):
#        c = Client()
#        response = c.get(reverse('calendar'), {'radius': 200})
#        self.assertEqual(response.status_code, 200)
#    
#    def test_calendar_with_city(self):
#        c = Client()
#        response = c.get(reverse('calendar'), {'city': 2})
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, 'для Los Angeles')
#=======================================================================================================================
