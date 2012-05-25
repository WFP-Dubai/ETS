### -*- coding: utf-8 -*- ####################################################
import os.path, subprocess, tempfile, platform
import StringIO
from optparse import make_option
from tkFileDialog import askopenfilename
from tkMessageBox import showinfo, showerror
from Tkinter import Tk

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from ets.utils import import_file
from ets.compress import decompress_json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TITLE = "Importing file"
FILETYPES = [
    ('compressed data files', '.data'),
    ('json data files', '.json')
]

class Command(BaseCommand):
    """
    Accepts a file as command-line argument. 
    Deserializes all data and save them.
    """
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file', dest='file_name', type='string', help='Imported file name'),
        make_option('-d', '--dir', dest='dir_name', type='string', help='Directory name'),
    )
    help = 'Imports file with serialized and compressed data'

    def handle(self, file_name=None, dir_name=None, *args, **options):
        
        verbosity = int(options.get('verbosity', 1))
        
        if verbosity >= 2:
            print "Importing file --> ", file_name.encode('utf-8')

        if file_name:
            try:
                with open(file_name) as f:
                    total = import_file(f)
                    if verbosity >= 2:
                        print "Totally saved objects --> ", total
                
            except TypeError:
                raise CommandError("Wrong file argument. It must be proper file name instead of %s" % file_name)

        root = Tk()
        root.withdraw()

        if dir_name:
            if not os.path.exists(dir_name):
                showerror(TITLE, "Wrong path to dir with installator: %s" % dir_name)
                exit()
        else:
            dir_name = BASE_DIR
        dir_name = os.path.abspath(dir_name)
    
        options = {
            'initialdir': dir_name,
            'title': "Please choose file with initial data",
            'filetypes': FILETYPES,
        }
    
        try:
            initialfile = (i for i in os.listdir(dir_name) if i.endswith(".data")).next()
            initialfile = os.path.join(dir_name, initialfile)
            if os.path.isfile(initialfile):
                options['initialfile'] = initialfile
                # ext = os.path.splitext(initialfile)[1]
                # index = (n for n, i in enumerate(FILETYPES) if i[1] == ext).next()
                # if index:
                #     item = FILETYPES.pop(index)
                #     FILETYPES.insert(0, item)
                #     options['filetypes'] = FILETYPES
        except StopIteration:
            pass

        data_file = askopenfilename(**options)
        
        if data_file:
            ext = os.path.splitext(data_file)[1]
            if ext == ".data":
                file_decompressed = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
                with open(os.path.normpath(data_file), 'r') as f:
                    data = decompress_json(f.read())
                    if not data:
                        showerror(TITLE, "Decompression is failed. Wrong data in %" % data_file)
                        exit()
                    file_decompressed.write(data)
                    file_decompressed.close()
                    data_file = file_decompressed.name

        # addition = {}
        # if platform.system() == "Windows":
        #     addition['shell'] = True
        output = StringIO.StringIO()
        errors = StringIO.StringIO()
        
        call_command('loaddata', data_file, stdout=output, stderr=errors)
                    
        if errors.getvalue():
            showerror(" ".join([TITLE, "error"]), errors.getvalue())

        if output.getvalue():
            showinfo(TITLE, output.getvalue())
            
        output.close()
        errors.close()

