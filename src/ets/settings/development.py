from datetime import *
# Django settings for ets project.
from .default import *

DATABASES['default'] = ALL_DB['default']
DATABASES['compas'] = ALL_DB['compas_test_pak']

COMPAS_STATION = u'ISBX002'

COUNTRIES = ('586', )

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  
DEBUG = True

TEMPLATE_LOADERS = (
  (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
  ),
)
