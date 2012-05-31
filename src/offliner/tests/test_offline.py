### -*- coding: utf-8 -*- ####################################################
import os.path
import datetime

from django.test import TestCase
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
import StringIO

import ets.models
from ets.tests.utils import TestCaseMixin
from ets.utils import import_file

class OfflinerTestCase(TestCaseMixin, TestCase):
    
    def setUp(self):
     
        super(OfflinerTestCase, self).setUp()

        self.client.login(username="admin", password="admin")
        self.user = User.objects.get(username="admin")
    
    def test_API(self):
        
        response = self.client.get(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX003'}))
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        self.assertContains(response, 'ISBX00311A', status_code=200)
        
        response = self.client.get(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX003', "start_date": "2012-01-01"}))
        self.assertEqual(response["Content-Type"], "application/json; charset=utf-8")
        self.assertContains(response, 'ISBX003', status_code=200)
        self.assertNotContains(response, 'ISBX00311A', status_code=200)

        f = open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server-import.json'))
        response = self.client.post(reverse("api_offline", kwargs={"warehouse_pk": 'ISBX002'}), data=f.read(), content_type='application/json')
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


class OfflineSyncTestCase(TestCase):
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        super(OfflineSyncTestCase, self).setUp()
        
        self.file_name = os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'test', 'ets_data.data'))
        
        #self.client.login(username='recepient', password='recepient')
        #self.user = ets.models.User.objects.get(username="recepient")
        #self.order = ets.models.Order.objects.get(pk='THEIRORDER')
    
    def test_import_file_command(self):
        """Tests ets.management.commands.import_file.Command"""
        
        #Try without file argument
        self.assertRaises(SystemExit, lambda: call_command('import_file'))
        
        #Ensure we don't have objects in database. for example warehouses
        self.assertEqual(ets.models.Warehouse.objects.count(), 0)
        
        call_command('import_file', file_name=self.file_name, verbosity=1)
        
        #Test we imported three warehouses
        self.assertEqual(ets.models.Warehouse.objects.count(), 3)


class ExportTestCase(TestCaseMixin, TestCase):
    
    def test_export_compas_command(self):
        """Tests ets.management.commands.export_compas.Command"""
        
        output = StringIO.StringIO()
        
        #Try with not existed COMPAS station argument
        call_command('export_compas', compas='wrong_compas', compress=True, stdout=output)
        output.seek(0)
        
        total = import_file(output)
        
        self.assertEqual(total, 14)

    def test_export_waybills_command(self):
        """Tests offliner.management.commands.export_waybills.Command"""
        
        output = StringIO.StringIO()

        call_command('export_waybills', user="dispatcher", passwd="dispatcher", stdout=output)
        output.seek(0)
        
        total = import_file(output)
        
        self.assertEqual(total, 2)

    def test_export_waybills_dispach_sign(self):
        waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")

        self.client.login(username='dispatcher', password='dispatcher')
        response = self.client.post(reverse('waybill_finalize_dispatch', kwargs={'waybill_pk': waybill.pk,}))
        self.assertEqual(response.status_code, 200)

        output = StringIO.StringIO()
        
        call_command('export_waybills', user="dispatcher", passwd="dispatcher", stdout=output)
        output.seek(0)
        
        total = import_file(output)
        
        self.assertEqual(total, 5)
        #self.assertEqual(ets.models.LogEntry.objects.all().order_by("action_time")[0].change_message, "")

    def test_export_waybills_receipt_sign(self):
        waybill = ets.models.Waybill.objects.get(pk="ISBX00312A")

        dispatcher = User.objects.get(username="dispatcher")
        dispatcher.person.receive = True
        dispatcher.person.save()
        
        self.client.login(username='dispatcher', password='dispatcher')
        response = self.client.post(reverse('waybill_finalize_receipt', kwargs={'waybill_pk': waybill.pk,}))
        self.assertEqual(response.status_code, 200)

        output = StringIO.StringIO()

        call_command('export_waybills', user="dispatcher", passwd="dispatcher", stdout=output)
        output.seek(0)
        
        total = import_file(output)
        
        self.assertEqual(total, 9)
        #self.assertEqual(ets.models.LogEntry.objects.all().order_by("action_time")[0].change_message, "")
