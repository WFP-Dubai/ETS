### -*- coding: utf-8 -*- ####################################################

from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

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
        from ets import utils
        utils.update_compas(compas, utils.import_partners, utils.import_places, utils.import_reasons, 
                            utils.import_persons, utils.import_stock, utils.import_order)

    def handle(self, compas='', *args, **options):
        from ets.models import Compas
        
        stations = Compas.objects.all()
        if compas:
            stations = stations.filter(pk=compas)
            
        for compas in stations:
            if not compas.is_sync_active():
                self.synchronize(compas=compas.pk)
