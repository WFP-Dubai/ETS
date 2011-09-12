# Django settings for ets project.
from .default import *

DEBUG = False

# Local settings for development / production
try:
    from local import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DATABASES = DatabasesFormDatabase(DEFAULT_DATABASE)