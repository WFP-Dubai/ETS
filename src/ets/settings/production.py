# Django settings for ets project.
from ets.settings.default import *

DEBUG = False
COMPRESS_ENABLED = True

# Local settings for development / production
try:
    from local import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DATABASES = DatabasesFormDatabase(DEFAULT_DATABASE)