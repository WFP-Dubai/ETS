### -*- coding: utf-8 -*- ####################################################

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core import serializers

from ets.utils import get_compas_data
from ets.compress import compress_json

class Command(BaseCommand):
    """
    Constructs all data imported from COMPAS.
    Serializes them and returns been compressed.
    Accept two arguments:
      
      --compas -- COMPAS station identifier
      --compress -- boolean. To be compressed or not
    
    """
    option_list = BaseCommand.option_list + (
        make_option('--compas', dest='compas',
            help='Tells the system to synchronize only this one compas station'),
        make_option('--compress', dest='compress', action="store_true",
            help='Tells the system to compress output json'),
    )
    help = 'Serializes data and commpresses them'

    def handle(self, *args, **options):
        
        compas = options.get('compas', None)
        compress = options.get('compress', False)
        
        data = get_compas_data(compas)
        
        data = serializers.serialize('json', data, use_decimal=False)
        
        if compress:
            data = compress_json(data)
        
        return data
