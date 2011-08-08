### -*- coding: utf-8 -*- ####################################################

import datetime
from functools import wraps

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError 
from django.contrib.auth.forms import AuthenticationForm
from django.core.management import call_command

import ets.models

class CommandTestCase(TestCase):
    
    #multi_db = True
    fixtures = ['compas.json', ]
    
    def test_sync_compas(self):
        call_command('sync_compas', nodelete=True)
        