### -*- coding: utf-8 -*- ####################################################

from optparse import make_option
import lockfile
import os
import logging

from django.core.management.base import BaseCommand
from django.db.utils import DatabaseError
from django.conf import settings

from ets.utils import update_compas
from ets.models import Compas

LOG_DIRECTORY = settings.LOG_DIRECTORY

class LockedBaseCommandMixin(object):

    lock_file_name = 'lock.lock'
    
    def execute(self, *args, **options):
        
        lock = lockfile.FileLock(os.path.join(settings.EGG_ROOT, self.lock_file_name))
        
        lock.acquire(60)
        
        try:
            super(LockedBaseCommandMixin, self).execute(*args, **options)
        finally:
            lock.release()


class Command(LockedBaseCommandMixin, BaseCommand):

    option_list = BaseCommand.option_list + ( 
        make_option('--compas', dest='compas', default='',
            help='Tells the system to synchronize only this one compas station'),
    )

    help = 'Import data from COMPAS stations'
    lock_file_name = 'sync_compas.lock'
    log_name = 'sync_compas.log'

    def synchronize(self, compas):
        update_compas(compas)

    def get_log_name(self):
        return os.path.join(LOG_DIRECTORY, self.log_name)
    
    def handle(self, compas='', *args, **options):
        
        with open(self.get_log_name(), 'w') as f:
            stations = Compas.objects.all()
            if compas:
                stations = stations.filter(pk=compas)
                
            for compas in stations:
                f.write("\nUpdating COMPAS: %s" % compas)
                
                try:
                    self.synchronize(compas=compas.pk)
                except Exception, err:
                    f.write(unicode(err))
                else:
                    f.write("\nsuccess")
