### -*- coding: utf-8 -*- ####################################################
from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User

import ets.models
from ets.utils import update_compas
from ets.templatetags.extra_tags import waybill_edit, waybill_reception, waybill_creation

class TagsTestCase(TestCase):
    
    multi_db = True
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        call_command('loaddata', 'compas.json', verbosity=0, commit=False, database='compas')
        update_compas()
        call_command('loaddata', 'development.json', verbosity=0, commit=False, database='default')
        
        self.user = User.objects.get(username="admin")
        self.waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        self.order = ets.models.Order.objects.get(pk='OURLITORDER')
    
    def test_waybill_edit(self):
        """Checks methods compress of waybill instance"""
        data = waybill_edit(self.waybill, self.user)
        self.assertTrue(data['success'])
        
    def test_waybill_reception(self):
        """Checks methods compress of waybill instance"""
        data = waybill_reception(self.waybill, self.user)
        self.assertTrue(not data['success'])
        
    def test_waybill_creation(self):
        """Checks methods compress of waybill instance"""
        data = waybill_creation(self.order, self.user)
        self.assertTrue(data['success'])