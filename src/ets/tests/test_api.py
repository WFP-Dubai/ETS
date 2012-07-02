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
        self.assertEqual(response["Content-Type"], "application/csv")
        self.assertContains(response, 'ISBX00211A', status_code=200)
        # One wabill
        response = self.client.get(reverse("api_waybills", kwargs={"slug": self.get_waybill().slug}))
        self.assertContains(response, 'ISBX00211A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        item = dict_reader.next()
        self.assertEqual(item['slug'], self.get_waybill().slug)
        # Waybills with destination and warehouse
        response = self.client.get(reverse("api_waybills", kwargs={"warehouse": self.get_waybill().order.warehouse.code, 
                                                                   "destination": self.get_waybill().destination.code}))
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'ISBX003', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")

        response = self.client.get(reverse("api_waybills", kwargs={'format': "excel"}))
        self.assertEqual(response["Content-Type"], "application/excel")
        self.assertContains(response, 'ISBX00211A', status_code=200)
        
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
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        item = dict_reader.next()
        self.assertEqual(item['waybill.order.code'], self.get_waybill().order.pk)
        # Loading details for some destination and some warehouse
        response = self.client.get(reverse("api_loading_details", kwargs={"warehouse": self.get_waybill().order.warehouse.code, 
                                                                    "destination": self.get_waybill().destination.code}))
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'ISBX003', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        
        #Super user has access to all data
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("api_loading_details"))
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 7)
        
        #Test user with special permissions
        user = User.objects.get(username="admin")
        user.is_superuser = False
        user.save()
        
        user.user_permissions.add(Permission.objects.get(codename="loadingetail_api_full_access"))
        
        response = self.client.get(reverse("api_loading_details"))
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 7)
        
        
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
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        item = dict_reader.next()
        self.assertEqual(item['code'], order.code)
        # Orders with destination and warehouse
        response = self.client.get(reverse("api_orders", kwargs={"warehouse": order.warehouse.code, 
                                                        "destination": order.consignee.warehouses.all()[0].code}))
        self.assertContains(response, 'ISBX002', status_code=200)
        self.assertContains(response, 'DOEAF', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        # test excel format
        response = self.client.get(reverse("api_orders", kwargs={'format': "excel"}))
        self.assertContains(response, 'OURLITORDER', status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
        
        
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
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        item = dict_reader.next()
        self.assertEqual(item['order.code'], order.code)
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

        #Test returned excel file
        response = self.client.get(reverse("api_stock_items", kwargs={"format": 'excel'}))
        self.assertContains(response, warehouse.code, status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
    
        # Stock items for one warehouse
        response = self.client.get(reverse("api_stock_items", kwargs={"warehouse": warehouse.code}))
        self.assertContains(response, warehouse.code, status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        item = dict_reader.next()
        self.assertEqual(item['warehouse.code'], warehouse.code)
        
        #Super user has access to all data
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("api_stock_items"))
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 7)
        
        #Test user with special permissions
        user = User.objects.get(username="admin")
        user.is_superuser = False
        user.save()
        
        user.user_permissions.add(Permission.objects.get(codename="stockitem_api_full_access"))
        
        response = self.client.get(reverse("api_stock_items"))
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 7)
    
    def test_warehouses(self):
        
        # All stock items
        response = self.client.get(reverse("api_warehouses"))
        self.assertContains(response, "ISBX002", status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        # Stock items for one warehouse
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        item = dict_reader.next()
        self.assertEqual(item['code'], "ISBX002")
        
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
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        item = dict_reader.next()
        self.assertEqual(item['origin_id'], "testme01231")
        self.assertEqual(len(list(dict_reader)), warehouse.stock_items.count()-1)

        # Stock items in excel
        response = self.client.get("?".join([reverse("api_stock_items", kwargs={'format': 'excel', "warehouse": warehouse.pk}), params.urlencode()]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_orders(self):
        # Orders related to user in csv
        response = self.client.get("?".join([reverse("api_orders"), "sSearch="]))
        self.assertContains(response, 'OURLITORDER', status_code=200)        
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 1)

        # Orders related to user in excel
        response = self.client.get("?".join([reverse("api_orders", kwargs={'format': "excel"}), "sSearch="]))
        self.assertContains(response, 'OURLITORDER', status_code=200)        
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_waybills(self):
        # All waybills in csv
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'user_related'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), ets.models.Waybill.objects.count())
        
        # All waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={ 'format': 'excel', 'filtering': 'user_related'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_dispatch_waybills(self):
        # All dispatch waybills in csv
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'dispatches'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ISBX00211A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), ets.models.Waybill.dispatches(self.user).count())

        # All dispatch waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={ 'format': 'excel', 'filtering': 'dispatches'}))
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
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), ets.models.Waybill.receptions(self.user).count())

        # All reception waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={ 'format': 'excel', 'filtering': 'receptions'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ISBX00311A', status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")

    def test_table_not_validated_dispatch_waybills(self):
        # All not validated waybills in csv
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'validate_dispatch'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 2)

        # All not validated waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={ 'format': 'excel', 'filtering': 'validate_dispatch'}))
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
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 1)

        # All validated waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={ 'format': 'excel', 'filtering': 'dispatch_validated'}))
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
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 1)
        # All validated waybills in csv
        waybill.receipt_validated=True
        waybill.save()
        response = self.client.get(reverse("api_waybills", kwargs={ 'filtering': 'receipt_validated'}))
        self.assertContains(response, waybill_pk, status_code=200)
        self.assertEqual(response["Content-Type"], "application/csv")
        result = StringIO.StringIO(response.content)
        dict_reader = csv.DictReader(result, dialect=csv.excel_tab)
        self.assertEqual(len(list(dict_reader)), 1)
        # All validated waybills in excel
        response = self.client.get(reverse("api_waybills", kwargs={ 'format': 'excel', 'filtering': 'receipt_validated'}))
        self.assertContains(response, waybill_pk, status_code=200)
        self.assertEqual(response["Content-Type"], "application/excel")
