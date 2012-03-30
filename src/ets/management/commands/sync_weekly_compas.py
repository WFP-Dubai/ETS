### -*- coding: utf-8 -*- ####################################################

from optparse import make_option
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.utils import DatabaseError
from django.conf import settings

from ets.utils import update_compas_info
from ets.models import Compas, ImportLogger

LOG_DIRECTORY = settings.LOG_DIRECTORY
MINIMUM_AGE = 5


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
        update_compas_info(compas)

    def handle(self, compas='', *args, **options):
        compas = Compas.objects.get(pk='PSHX001')
        self.synchronize(compas=compas.pk)
