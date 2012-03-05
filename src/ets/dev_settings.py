# Django settings for ets project.
from ets.settings import *

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  
TEMPLATE_LOADERS = (
  (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
  ),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request':{
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': True,
        },
        'ho.pisa': {
            'handlers': ['console',],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}


MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

DEBUG = True
TEMPLATE_DEBUG = True

COMPRESS_ENABLED = False

SERVE_STATIC = False

DEBUG_TOOLBAR_PANELS = (
        #'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        #'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        #'debug_toolbar.panels.cache.CacheDebugPanel',
        #'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.sqlite3',
}

# Local settings for development / production
try:
    from local_settings import *
except ImportError:
    pass

ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DATABASES = DatabasesFormDatabase(DEFAULT_DATABASE)
