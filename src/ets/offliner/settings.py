# Django settings for ets project.
from ets.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = False

DATABASES = {
    'default': DEFAULT_DATABASE,
}

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
