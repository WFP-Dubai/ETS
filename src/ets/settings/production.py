# Django settings for ets project.
from .default import *

DEBUG = False
DISABLE_EXPIERED_LTI = True

# Local settings for development / production
try:
    from local import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
