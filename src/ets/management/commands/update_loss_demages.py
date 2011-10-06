### -*- coding: utf-8 -*- ####################################################

from ets.utils import update_loss_damage
from .sync_compas import Command as UpdateCompas

class Command(UpdateCompas):

    help = 'Import data from COMPAS stations with loss damage data'

    def update_main(self, using):
        update_loss_damage(using)
        

