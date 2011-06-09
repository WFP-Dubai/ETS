from datetime import *
# Django settings for ets project.
from  settings_default import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES['default'] = ALL_DB['default_tc_pak']
DATABASES['compas'] = ALL_DB['compas_test_pak']
COMPAS_STATION = u'ISBX002'
COUNTRIES = ['586']
MEDIA_ROOT = os.path.join( os.path.dirname( __file__ ), 'media' )
MEDIA_URL = '/ets/media'
SESSION_COOKIE_NAME = 'ets-demo'
#date of the start of ltis to import
DISABLE_EXPIERED_LTI = DEBUG
MAX_DATE = '2010-01-01'
#IN_PRODUCTION=True
