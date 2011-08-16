# Django settings for ets project.
from .default import *

DATABASES['default'] = ALL_DB['default']
DATABASES['compas'] = ALL_DB['dev_compas']

COMPAS_STATION = u'ISBX002'

COUNTRIES = ('586', )

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  
TEMPLATE_LOADERS = (
  (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
  ),
)

DEBUG = True
DISABLE_EXPIERED_LTI = True
TEMPLATE_DEBUG = True