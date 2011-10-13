### -*- coding: utf-8 -*- ####################################################

from ets.models import LossDamageType
from .sync_compas import Command as UpdateCompas

from ets.utils import send_dispatched, send_received, import_stock

class Command(UpdateCompas):

    help = 'Submits waybills and updates stocks'

    def synchronize(self, compas):
        send_dispatched(compas)
        send_received(compas)
        import_stock(compas)

        
