### -*- coding: utf-8 -*- ####################################################

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.utils import DatabaseError

from ets.utils import update_compas
from ets.models import Compas

class Command(BaseCommand):

    option_list = BaseCommand.option_list + ( 
        make_option('--compas', dest='compas', default='',
            help='Tells the system to synchronize only this one compas station'),
    )

    help = 'Import data from COMPAS stations'

    def synchronize(self, compas):
        update_compas(compas)

    def handle(self, compas='', *args, **options):
        
        verbosity = int(options.get('verbosity', 1))
        
        stations = Compas.objects.all()
        if compas:
            stations = stations.filter(pk=compas)
            
        for compas in stations:
            if verbosity >= 2:
                print "Updating compas: %s" % compas
            
            try:
                self.synchronize(compas=compas.pk)
            except Exception, err:
                if verbosity >= 2:
                    print err
