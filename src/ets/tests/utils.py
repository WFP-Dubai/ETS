### -*- coding: utf-8 -*- ####################################################

from functools import wraps

from django.conf import settings
from django.core.management import call_command

from ets import utils

def change_settings(func, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        old_settings = {}
        for name, value in kwargs:
            old_settings[name] = getattr(settings, name)
            setattr(settings, value)
            
        result = func(*args, **kwargs)
        
        for name, value in kwargs:
            setattr(settings, old_settings[name])
        
        return result
    
    return wrapper

class TestCaseMixin(object):
    
    #multi_db = True
    compas = 'ISBX002'
    fixtures = ('db_compas.json', 'warehouse.json', 'groups.json', 'permissions.json')
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        call_command('loaddata', 'compas.json', verbosity=0, commit=False, database=self.compas)
        utils.update_compas(self.compas, utils.import_partners, utils.import_places, utils.import_reasons, 
                      utils.import_persons, utils.import_stock, utils.import_order)
        call_command('loaddata', 'development.json', verbosity=0, commit=False, database='default')
