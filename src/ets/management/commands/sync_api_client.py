django.core.management.base import BaseCommand

from ets.api.client import *


class Command(BaseCommand):

    help = 'Synchronizes data for clients'

    def handle(self, *args, **options):
        send_new()
        get_informed()
        get_delivered()
        get_receiving()
        send_informed()
        send_delivered()