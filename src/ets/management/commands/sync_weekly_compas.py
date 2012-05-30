### -*- coding: utf-8 -*- ####################################################

from django.core.management.base import BaseCommand
from django.conf import settings

from ets import utils
from ets.models import Compas

LOG_DIRECTORY = settings.LOG_DIRECTORY
MINIMUM_AGE = 5


class Command(BaseCommand):
    """
    Import data from COMPAS stations. 
    Accepts following arguments:
        
        --compas -- COMPAS station identifier (i.e. ISBX002 for example)
        
    """
    help = 'Import data from COMPAS stations'
    
    def handle(self, *args, **options):
        compas = Compas.objects.get(pk='PSHX001')
        utils.update_compas(compas.pk, utils.import_partners, utils.import_places, utils.import_reasons)
