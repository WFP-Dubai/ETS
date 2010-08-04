import os,sys
#pathname, scriptname = os.path.split(sys.argv[0])
current_server = os.path.dirname(os.path.abspath(__file__))

#current_server = os.path.abspath(pathname)
#print  current_server_dir
sys.path.append('config')

from settings_default import *

configs = {
	'C:\\epic\\ets':'set_prod',
	'C:\\epic\\training\\ets':'set_test',
	'C:\\ETS\\dev_env\\ets':'sami',
	'/Users/tobias/projects/epic/ets':'tobymb',
	'/Users/carlander/projects/epic/ets':'tobymp',
}
config_module = __import__('%s' % configs[current_server], globals(), locals(), 'ets')


for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)
