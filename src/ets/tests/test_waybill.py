### -*- coding: utf-8 -*- ####################################################

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

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
    

class ClientWaybillTestCase(TestCase):
    
    #multi_db = True
    fixtures = ['development.json', ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.client.login(username='admin', password='admin')
        self.user = User.objects.get(username="admin")
     
    #===================================================================================================================
    # def tearDown(self):
    #    "Hook method for deconstructing the test fixture after testing it."
    #===================================================================================================================
    
    def test_index(self):
        response = self.client.get(reverse('select_action'))
        self.assertEqual(response.status_code, 200)
        
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
