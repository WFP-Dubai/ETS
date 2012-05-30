### -*- coding: utf-8 -*- ####################################################
import urllib2

from django.core.management.base import BaseCommand

from ets.models import Waybill

class Command(BaseCommand):

    help = 'Sends created and signed waybills to central server'

    def handle(self, compas='', *args, **options):
        
        verbosity = int(options.get('verbosity', 1))
        
        for waybill in Waybill.objects.filter(transport_dispach_signed_date__isnull=False,
                                              offline_sync__date__isnull=True):
            data = waybill.serialize()
            return urllib2.urlopen(urllib2.Request('api_offline', data, {
                    'Content-Type': 'application/json; charset=utf-8',
            }))
            
            
            if verbosity >= 2:
                print "Updating compas: %s" % compas
            self.synchronize(compas=compas.pk)
