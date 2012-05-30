# -*- coding: utf-8 -*-
import os.path, subprocess, sys, tempfile, platform
from tkFileDialog import askopenfilename
from tkMessageBox import showinfo, showerror
from Tkinter import Tk


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR = "src/ets/fixtures"
INSTANCE_COMMANDS = ("instance", "instance-script.py", "instance.exe")
TITLE = "Importing file"
FILETYPES = [
    ('compressed data files', '.data'),
    ('json data files', '.json')
]

def get_command():
    for command in INSTANCE_COMMANDS:
        path_to_instance = os.path.join(BASE_DIR, 'bin', command)
        if os.path.exists(path_to_instance):
            return path_to_instance         

if __name__ == '__main__':
    root = Tk()
    root.withdraw()

    if len(sys.argv) > 1:
        installator_dir = sys.argv[1]
        if not os.path.exists(installator_dir):
            showerror(TITLE, "Wrong path to dir with installator: %s" % installator_dir)
            exit()
    else:
        installator_dir = BASE_DIR
    installator_dir = os.path.abspath(installator_dir)
    
    options = {
        'initialdir': installator_dir,
        'title': "Please choose file with initial data",
        'filetypes': FILETYPES,
    }
    
    try:
        initialfile = (i for i in os.listdir(installator_dir) if i.endswith(".data")).next()
        initialfile = os.path.join(installator_dir, initialfile)
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
        command = get_command()
        if not command:
            showerror(TITLE, "Django instance doesn't exist")
            exit()
        
        ext = os.path.splitext(data_file)[1]
        if ext == ".data":
            file_decompressed = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
            with open(os.path.normpath(data_file), 'r') as f:
                sys.path.append(os.path.join(BASE_DIR, "src/ets"))        
                from compress import decompress_json
                data = decompress_json(f.read())
                if not data:
                    showerror(TITLE, "Decompression is failed. Wrong data in %" % data_file)
                    exit()
                file_decompressed.write(data)
                file_decompressed.close()
                data_file = file_decompressed.name

        addition = {}
        if platform.system() == "Windows":
            addition['shell'] = True 

        loaddata = subprocess.Popen([command, "loaddata", data_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, **addition)
        result, error = loaddata.communicate()
        if ext == ".data":
            os.remove(file_decompressed.name)

        if result:
            showinfo(TITLE, result)
        elif error:
            showerror("Importing file error", error)
        
