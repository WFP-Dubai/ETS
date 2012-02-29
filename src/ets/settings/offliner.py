# Django settings for ets project.
from ets.settings.default import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False

DATABASES = {
    'default': DEFAULT_DATABASE,
}
