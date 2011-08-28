### -*- coding: utf-8 -*- ####################################################

from django.core.management.base import BaseCommand

from ets.utils import update_compas
from ets.models import Compas

class Command(BaseCommand):

    help = 'Import data from COMPAS stations'

    def handle(self, *args, **options):
        
        for compas in Compas.objects.all():
            update_compas(using=compas.pk)
