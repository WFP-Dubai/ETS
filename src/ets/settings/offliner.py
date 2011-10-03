# Django settings for ets project.
import os.path

from .default import *

# Local settings for development / production
try:
    from local_settings import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DATABASES = DatabasesFormDatabase(DEFAULT_DATABASE)
