from datetime import *
# Django settings for ets project.
from  settings_default import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES['default'] = ALL_DB['default_tc_mb']
DATABASES['compas'] = ALL_DB['compas_test_pal']
