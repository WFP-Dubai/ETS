### -*- coding: utf-8 -*- ####################################################

from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from ets.utils import (update_compas, 
                       import_persons, import_stock, import_order,
                       import_partners, import_places, import_reasons) 
from ets.models import Compas

LOG_DIRECTORY = settings.LOG_DIRECTORY



class Command(BaseCommand):
    """
    Import data from COMPAS stations. 
    Accepts following arguments:
        
        --compas -- COMPAS station identifier (i.e. ISBX002 for example)
        
    """
    option_list = BaseCommand.option_list + ( 
        make_option('--compas', dest='compas', default='',
            help='Tells the system to synchronize only this one compas station'),
    )

    help = 'Import data from COMPAS stations'
    
    def synchronize(self, compas):
        """Exact method to proceed synchronization"""
        update_compas(compas, import_partners, import_places, import_reasons, import_persons, import_stock, import_order)

    def handle(self, compas='', *args, **options):
        
        stations = Compas.objects.all()
        if compas:
            stations = stations.filter(pk=compas)
            
        for compas in stations:
            if not compas.is_sync_active():
                self.synchronize(compas=compas.pk)
