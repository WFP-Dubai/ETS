import os.path, base64

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import ets.models
from ets.tests.utils import TestCaseMixin

class OfflinerTestCase(TestCaseMixin, TestCase):
    
    def setUp(self):
     
        super(OfflinerTestCase, self).setUp()

        self.client.login(username="admin", password="admin")
        self.user = User.objects.get(username="admin")

        auth = '%s:%s' % ('admin', 'admin')
        auth = 'Basic %s' % base64.encodestring(auth)
        auth = auth.strip()
        self.extra = {
            'HTTP_AUTHORIZATION': auth,
        }
    
    def test_API(self):
        
        response = self.client.get(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX003'}), {}, **self.extra)
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        self.assertContains(response, 'ISBX00311A', status_code=200)
        
        response = self.client.get(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX003', "start_date": "2012-01-01"}), {}, **self.extra)
#        response = self.client.get(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX003', "start_date": "2012-01-01"}))
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        self.assertContains(response, 'ISBX003', status_code=200)
        self.assertNotContains(response, 'ISBX00311A', status_code=200)

        f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server-import.json'))
        response = self.client.post(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX002'}), data=f.read(), content_type='application/json', **self.extra)
#        response = self.client.post(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX002'}), data=f.read(), content_type='application/json')
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        waybill = get_object_or_404(ets.models.Waybill, pk="ISBX00211G")
        self.assertEqual(waybill.pk, 'ISBX00211G')
        
    def test_import_data(self):
        f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server-export.json'))
        response = self.client.post(reverse("import_data"), data={'file': f})
        self.assertEqual(response.status_code, 302)  
        waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        self.assertEqual(waybill.transport_driver_name, "Mahmud")

    def test_export_data(self):
        warehouse = ets.models.Warehouse.objects.get(pk="ISBX002")
        response = self.client.get(reverse("export_data"), data={'warehouse': warehouse.pk})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('api_offline', kwargs={"warehouse_pk": warehouse.pk}))

    def test_export_data_protect(self):
        warehouse = ets.models.Warehouse.objects.get(pk="ISBX002")
        response = self.client.get(reverse("export_data"), data={'warehouse': warehouse.pk})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('api_offline', kwargs={"warehouse_pk": warehouse.pk}))
