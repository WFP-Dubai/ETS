### -*- coding: utf-8 -*- ####################################################

from django.core.management.base import BaseCommand

from ets.utils import update_compas


class Command(BaseCommand):

    help = 'Synchronizes data with compas database'

    def handle(self, *args, **options):
        update_compas()
