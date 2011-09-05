### -*- coding: utf-8 -*- ####################################################
from django.test import TestCase
from django.contrib.auth.models import User

import ets.models
from ets.templatetags.extra_tags import waybill_edit, waybill_reception, waybill_creation, waybill_delete

from .utils import TestCaseMixin

class TagsTestCase(TestCaseMixin, TestCase):
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        super(TagsTestCase, self).setUp()
            
        self.user = User.objects.get(username="dispatcher")
        self.waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        self.order = ets.models.Order.objects.get(pk='OURLITORDER')
    
    def test_waybill_edit(self):
        """Checks methods compress of waybill instance"""
        data = waybill_edit(self.waybill, self.user)
        self.assertTrue(data['success'])
        
    def test_waybill_reception(self):
        """Checks methods compress of waybill instance"""
        self.user = User.objects.get(username="recepient")
        data = waybill_reception(self.waybill, self.user)
        self.assertTrue(data['success'])
        
    def test_waybill_creation(self):
        """Checks methods compress of waybill instance"""
        data = waybill_creation(self.order, self.user)
        self.assertTrue(data['success'])
        
    def test_waybill_delete(self):
        """Checks methods compress of waybill instance"""
        data = waybill_delete(self.waybill, self.user)
        self.assertTrue(data['success'])