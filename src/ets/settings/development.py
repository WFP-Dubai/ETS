# Django settings for ets project.
from .default import *

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  
TEMPLATE_LOADERS = (
  (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
  ),
)

DEBUG = True
TEMPLATE_DEBUG = True

# Local settings for development / production
try:
    from local import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DATABASES = DatabasesFormDatabase(DEFAULT_DATABASE)

COMPRESS_ENABLED = False

CONSUMER_KEY="mine_key"
CONSUMER_SECRET="sdvvfddsvabapb_Dsfih7gb"
