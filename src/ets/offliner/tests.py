import datetime
import os.path

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import ets.models
from ets.tests.utils import TestCaseMixin

class OfflinerTestCase(TestCaseMixin, TestCase):
    
    def setUp(self):
     
        super(OfflinerTestCase, self).setUp()

        self.client.login(username="admin", password="admin")
        self.user = User.objects.get(username="admin")
    
    def test_API(self):
        
        response = self.client.get(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX002'}))
        self.assertEqual(response["Content-Type"], "text/json; charset=utf-8")
        self.assertContains(response, 'ISBX00211A', status_code=200)
        
        response = self.client.get(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX002', "start_date": "2012-01-01"}))
        self.assertEqual(response["Content-Type"], "text/json; charset=utf-8")
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertNotContains(response, 'ISBX00211A', status_code=200)
        
    def test_import_data(self):
        f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server-export.json'))
        response = self.client.post(reverse("import_data"), data={'file': f})
        self.assertEqual(response.status_code, 302)  
        waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        self.assertEqual(waybill.transport_driver_name, "Mahmud")
        
    
    