from datetime import *
# Django settings for ets project.
from  settings_default import *
print 'Settings TC MP'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES['default'] = ALL_DB['default_tc_pak']
DATABASES['compas'] = ALL_DB['compas_test_pak']
#COMPAS_STATION=u'JERX001'
COMPAS_STATION=u'ISBX002'
#COUNTRIES=['275','376']
COUNTRIES=['586']
