### -*- coding: utf-8 -*- ####################################################
from django.test import TestCase
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.core.management import call_command

import ets.models
from ets.tests.utils import TestCaseMixin

class OrderTestCase(TestCaseMixin, TestCase):
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        super(OrderTestCase, self).setUp()
        
        self.client.login(username='recepient', password='recepient')
        self.user = ets.models.User.objects.get(username="recepient")
        self.order = ets.models.Order.objects.get(pk='THEIRORDER')
    
    def test_order_list(self):
        """ets.views.order_list"""
        self.client.login(username='dispatcher', password='dispatcher')
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['object_list'].count(), 1)

    def test_order_detail(self):
        """Order's detail page"""
        response = self.client.get(reverse('order_detail', kwargs={'object_id': self.order.pk,}))
        self.assertEqual(response.status_code, 200)
    
    def test_order_percentage(self):
        self.assertEqual(self.order.percentage, 0)
        call_command('order_percentage')
        self.order = ets.models.Order.objects.get(pk='THEIRORDER')
        self.assertEqual(self.order.percentage, 100)


