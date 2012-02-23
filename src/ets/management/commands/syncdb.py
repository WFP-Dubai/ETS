"""
Overridden syncdb command
"""

from django.core.management.commands.syncdb import Command as DjangoSyncDB
from django.db import DEFAULT_DB_ALIAS

from south.db import dbs
from south.management.commands.syncdb import Command as SouthSyncDB


class Command(SouthSyncDB):
    """
    Special version of South' syncdb command to make it work with our compas stations.
    """
    def handle_noargs(self, migrate_all=False, database=DEFAULT_DB_ALIAS, **options):
        if database in dbs:
            super(Command, self).handle_noargs(migrate_all=migrate_all, database=database, **options)
        else:
            DjangoSyncDB().execute(database=database, **options)
