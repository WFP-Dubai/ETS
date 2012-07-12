### -*- coding: utf-8 -*- ####################################################
import csv
import StringIO
import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.http import QueryDict

#from ets.models import Waybill, LoadingDetail, LtiOriginal, EpicStock, DispatchPoint, LtiWithStock, urllib2
import ets.models
#from ets.models import Waybill, LtiOriginal, EpicStock, Warehouse,
from ets.tests.utils import TestCaseMixin


class ApiServerTestCase(TestCaseMixin, TestCase):
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."        
        super(ApiServerTestCase, self).setUp()

        self.client.login(username="dispatcher", password="dispatcher")
        self.user = User.objects.get(username="dispatcher")
 
    
    def get_waybill(self):
        return ets.models.Waybill.objects.get(pk="ISBX00211A")
        
    def test_get_waybills(self):

        # All waybills
        response = self.client.get(reverse("api_waybills"))
        self.assertEqual(response["Content-Type"], "application/excel")
        self.assertContains(response, 'ISBX00211A', status_code=200)
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'ISBX003', status_code=200)
        
    def test_get_loading_details(self):

        # All Loading details
        response = self.client.get(reverse("api_loading_details"))
        self.assertContains(response, 'ISBX00211A1', status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
        
        #Super user has access to all data
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("api_loading_details"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ISBX00211A1', status_code=200)
        
        #Test user with special permissions
        user = User.objects.get(username="admin")
        user.is_superuser = False
        user.save()
        
        user.user_permissions.add(Permission.objects.get(codename="loadingetail_api_full_access"))
        
        response = self.client.get(reverse("api_loading_details"))
        self.assertEqual(response.status_code, 200)
        
    def test_get_orders(self):

        order = ets.models.Order.objects.get(pk='OURLITORDER')
        # All orders
        response = self.client.get(reverse("api_orders"))
        self.assertContains(response, 'OURLITORDER', status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
        
    def test_get_order_items(self):

        # All order items
        response = self.client.get(reverse("api_order_items"))
        self.assertEqual(response["Content-Type"], "application/excel")
        self.assertContains(response, 'OURLITORDER', status_code=200)
        
    def test_get_stock_items(self):
        
        warehouse = ets.models.Warehouse.objects.get(pk='ISBX002')
        # All stock items
        response = self.client.get(reverse("api_stock_items"))
        self.assertContains(response, warehouse.code, status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")

        # Stock items for one warehouse
        response = self.client.get(reverse("api_stock_items", kwargs={"warehouse": warehouse.code}))
        self.assertContains(response, warehouse.code, status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
        
        #Super user has access to all data
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("api_stock_items"))
        self.assertEqual(response.status_code, 200)
        
    def test_warehouses(self):
        
        response = self.client.get(reverse("api_warehouses"))
        self.assertContains(response, "ISBX002", status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
        
    def test_table_stock_items(self):
        # All stock items
        warehouse = ets.models.Warehouse.objects.get(pk="ISBX003")
        params = QueryDict('', mutable=True)
        _params = {
            'sSearch': "",
            'sortable': "quantity_gross"
        }
        params.update(_params)
        response = self.client.get("?".join([reverse("api_stock_items", kwargs={"warehouse": warehouse.pk}), params.urlencode()]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/excel")
        self.assertContains(response, "testme01231")

    def test_table_warehouses(self):
        self.client.login(username="admin", password="admin")
        # All warehouses
        params = QueryDict('', mutable=True)
        _params = {
            'sSearch': "",
            'sortable': "start_date"
        }
        params.update(_params)
        response = self.client.get("?".join([reverse("api_warehouses"), params.urlencode()]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_orders(self):
        # Orders related to user in csv
        response = self.client.get("?".join([reverse("api_orders"), "sSearch="]))
        self.assertContains(response, 'OURLITORDER', status_code=200)        
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_waybills(self):
        
        # All waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={'filtering': 'user_related'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_dispatch_waybills(self):

        # All dispatch waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={'filtering': 'dispatches'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ISBX00211A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_reception_waybills(self):
        # All reception waybills in csv
        person = ets.models.Person.objects.get(username=self.user.username)
        person.receive = True
        person.save()
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'receptions'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ISBX00311A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
        
        # All reception waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={'filtering': 'receptions'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ISBX00311A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_not_validated_dispatch_waybills(self):
        self.client.login(username='admin', password='admin')

        # All not validated waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={'filtering': 'validate_dispatch'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_validated_dispatch_waybills(self):
        # All validated waybills in csv
        self.client.login(username='admin', password='admin')
        waybill_pk = 'ISBX00311A'
        waybill = ets.models.Waybill.objects.get(pk=waybill_pk)
        waybill.validated=True
        waybill.save()
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'dispatch_validated'}))
        self.assertContains(response, waybill_pk, status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_validate_receipt_waybills(self):
        # All not validated waybills
        waybill_pk = 'ISBX00211A'
        waybill = ets.models.Waybill.objects.get(pk=waybill_pk)
        self.client.login(username='admin', password='admin')
        waybill.transport_dispach_signed_date = datetime.date.today()
        waybill.receipt_signed_date = datetime.date.today()
        waybill.save()
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'validate_receipt'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/excel")
        # All validated waybills in csv
        waybill.receipt_validated=True
        waybill.save()
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'receipt_validated'}))
        self.assertContains(response, waybill_pk, status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
        