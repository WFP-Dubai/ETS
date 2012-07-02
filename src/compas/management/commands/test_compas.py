### -*- coding: utf-8 -*- ####################################################

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.utils import load_backend


class Command(BaseCommand):
    """'Tests connection to COMPAS stations'"""
    option_list = BaseCommand.option_list + ( 
        make_option('--engine', dest='db_engine', default='django.db.backends.oracle', help='Database engine'),
        make_option('--name', dest='db_name', help='Database name'),
        make_option('--user', dest='db_user', help='Database user name'),
        make_option('--password', dest='db_password', help='Database user password'),
        make_option('--host', dest='db_host', help='Database host'),
        make_option('--port', dest='db_port', default='', help='Database port'),
    )
    
    help = 'Tests connection to COMPAS stations'

    def handle(self, db_engine, db_name, db_user, db_password, db_host, db_port, *args, **options):
        
        verbosity = int(options.get('verbosity', 1))
        
        backend = load_backend(db_engine)
        conn = backend.DatabaseWrapper({
                'NAME': db_name,
                'ENGINE': db_engine,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': db_port,
                'OPTIONS': {},
        }, 'test_connection')
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM organizations;")
            cursor.execute("SELECT COUNT(*) FROM organizations;")
            cursor.execute("SELECT COUNT(*) FROM epic_geo;")
            cursor.execute("SELECT COUNT(*) FROM epic_geo;")
            cursor.execute("SELECT COUNT(*) FROM epic_persons;")
            cursor.execute("SELECT COUNT(*) FROM epic_persons;")
        except Exception, err:
            if verbosity >= 2:
                print err
