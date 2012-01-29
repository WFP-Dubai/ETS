### -*- coding: utf-8 -*- ####################################################

from optparse import make_option
import lockfile
import os
import logging
import time
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.utils import DatabaseError
from django.conf import settings

from ets.utils import update_compas
from ets.models import Compas

LOG_DIRECTORY = settings.LOG_DIRECTORY
MINIMUM_AGE = 30

class LockedBaseCommandMixin(object):

    lock_file_name = 'lock.lock'
    
    def execute(self, *args, **options):
        
        lock = lockfile.FileLock(os.path.join(settings.EGG_ROOT, self.lock_file_name))
        
        try:
            lock.acquire(timeout=30)    # wait up to 60 seconds
        except lockfile.LockTimeout:
            
            lock_time = datetime.fromtimestamp(os.path.getctime(lock.path))
            if lock_time + datetime.timedelta(minutes=MINIMUM_AGE) <= datetime.datetime.now():
                lock.break_lock()
                lock.acquire()
            
            raise
        
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
        
        self.logs = []
        
        self.logs.append("\nDate: %s" % datetime.now())
        
        stations = Compas.objects.all()
        if compas:
            stations = stations.filter(pk=compas)
            
        for compas in stations:
            self.logs.append("\nUpdating COMPAS: %s" % compas)
            
            try:
                self.synchronize(compas=compas.pk)
            except Exception, err:
                self.logs.append("\n%s" % unicode(err))
            else:
                self.logs.append("\nsuccess")
    
        with open(self.get_log_name(), 'w') as f:
            f.writelines(self.logs)
        