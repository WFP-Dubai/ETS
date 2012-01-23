### -*- coding: utf-8 -*- ####################################################

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from ets.utils import import_file

class Command(BaseCommand):
    
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file', dest='file_name', type='string', help='Imported file name'),
    )
    help = 'Imports file with serialized and compressed data'

    def handle(self, file_name, *args, **options):
        
        verbosity = int(options.get('verbosity', 1))
        
        if verbosity >= 2:
            print "Importing file --> ", file_name.encode('utf-8')
        
        try:
            with open(file_name) as f:
                total = import_file(f)
                if verbosity >= 2:
                    print "Totally saved objects --> ", total
                
        except TypeError:
            raise CommandError("Wrong file argument. It must be proper file name instead of %s" % file_name)
        