import os,sys
pathname, scriptname = os.path.split(sys.argv[0])
current_server = os.path.dirname(os.path.abspath(__file__))
sys.path.append('config')

try:
	from settings_default import *
	
	configs = {
		'C:\\epic\\ets':'set_prod',
		'C:\\epic\\training\\ets':'set_test',
		'C:\\ETS\\dev_env\\ets':'sami',
		'/Users/tobias/projects/epic/ets':'tobymb',
		'/Users/carlander/projects/epic/ets':'tobymp',
	}
	config_module = __import__('%s' % configs[current_server], globals(), locals(), 'ets')
	print config_module
	for setting in dir(config_module):
	    if setting == setting.upper():
	        locals()[setting] = getattr(config_module, setting)
except:
    try:
        from settings_local import *
    except ImportError:
        pass
        
print MEDIA_URL