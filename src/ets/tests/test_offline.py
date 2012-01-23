### -*- coding: utf-8 -*- ####################################################
import os.path

from django.test import TestCase
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.conf import settings

import ets.models
from .utils import TestCaseMixin

class OfflineSyncTestCase(TestCase):
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        super(OfflineSyncTestCase, self).setUp()
        
        self.file_name = os.path.normpath(os.path.join(settings.MEDIA_ROOT, 'test', 'ets_data.data'))
        
        #self.client.login(username='recepient', password='recepient')
        #self.user = ets.models.User.objects.get(username="recepient")
        #self.order = ets.models.Order.objects.get(pk='THEIRORDER')
    
    def test_import_file_command(self):
        """ets.views.order_list"""
        
        #Try without file argument
        self.assertRaises(SystemExit, lambda: call_command('import_file', file_name=None))
        
        #Ensure we don't have objects in database. for example warehouses
        self.assertEqual(ets.models.Warehouse.objects.count(), 0)
        
        call_command('import_file', file_name=self.file_name, verbosity=1)
        
        #Test we imported three warehouses
        self.assertEqual(ets.models.Warehouse.objects.count(), 3)
        
    def test_order_detail(self):
        """Order's detail page"""
        response = self.client.get(reverse('order_detail', kwargs={'object_id': self.order.pk,}))
        self.assertEqual(response.status_code, 200)
    
    def test_order_percentage(self):
        response = self.client.get(reverse('order_detail', kwargs={'object_id': self.order.pk,}))
        self.assertEqual(response.context['object'].get_percent_executed(), 100)

    def test_order_percentage_null(self):
        self.client.login(username='dispatcher', password='dispatcher')
        
        self.order = ets.models.Order.objects.get(pk='OURLITORDER')
        response = self.client.get(reverse('order_detail', kwargs={'object_id': self.order.pk,}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].get_percent_executed(), 0)       
