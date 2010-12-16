import os,sys
current_server = os.path.dirname(os.path.abspath(__file__))
sys.path.append('config')

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
