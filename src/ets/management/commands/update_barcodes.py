### -*- coding: utf-8 -*- ####################################################
from django.core.management.base import BaseCommand

from ets.models import Waybill

class Command(BaseCommand):
    """Count percentage of order executing"""
    
    help = 'Update barcodes of waybills'

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', 1)
        
        total = 0
        for waybill in Waybill.objects.all():
            waybill.save()
            if verbosity > 1:
                print "%s\t%s" % (total, waybill.pk)
