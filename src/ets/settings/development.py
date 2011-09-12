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
DISABLE_EXPIERED_LTI = True
TEMPLATE_DEBUG = True

# Local settings for development / production
try:
    from local import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DISABLE_EXPIERED_LTI = DEBUG
DATABASES = DatabasesFormDatabase(DEFAULT_DATABASE)