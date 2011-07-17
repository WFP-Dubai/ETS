# Django settings for ets project.

# This module is available as common_settings from projects' settings module.
# It contains settings used in all projects.

import os.path
from django.conf import global_settings

PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')
EGG_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../')

ugettext = lambda s: s

DEBUG = False

MANAGERS = ( 
    # ('Your Name', 'your_email@domain.com'),
 )
ADMINS = ( 
    # ('Your Name', 'your_email@domain.com'),
 )


ALL_DB = {
    'default': {
        'NAME': 'db',
        'ENGINE': 'django.db.backends.sqlite3',
        'USER': '',
        'PASSWORD': '',
    },
    'default_tc_pak': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wb_pak',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }, 
    'default_tc_pak_rem': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wb_pak',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '10.11.208.20',
        'PORT': '',
    },
    'default_test_pak': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waybill_pak',
        'USER': 'root',
        'PASSWORD': 'trackme',
        'HOST': '10.11.208.20',
        'PORT': '',
    },
    'compas_test_pak': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '10.11.70.50/ISBX002',
        'USER': 'TESTISBX002',
        'PASSWORD': 'TESTISBX002',
        'HOST': '10.11.70.50',
        'PORT': '',
    },
    'default_tc_mb': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waybill',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
    'compas_test_pal': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '10.11.216.4/JERX001',
        'USER': 'TESTJERX001',
        'PASSWORD': 'TESTJERX001',
        'HOST': '10.11.216.4',
        'PORT': '',
    },
    'default_tc_mp': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waybill',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
    'compas_test_rome': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '10.11.32.26/CMPS',
        'USER': 'bw_reader',
        'PASSWORD': 'readme',
        'HOST': '10.11.32.26',
        'PORT': '',
    },
    'compas_prod_pal': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': '10.11.216.4/JERX001',
        'USER': 'opt_epic',
        'PASSWORD': 'opt_epic',
        'HOST': '10.11.33.199',
        'PORT': '',
    },
    'default_serafino': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'waybill',
        'USER': 'postgres',
        'PASSWORD': 'postgres_password',
        'HOST': 'localhost',
        'PORT': '',
    },
    'offline_serafino': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'offline',
        'USER': 'postgres',
        'PASSWORD': 'postgres_password',
        'HOST': 'localhost',
        'PORT': '',
    },
    'default_training_pal': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waybilltraining',
        'USER': 'root',
        'PASSWORD': 'epic',
        'HOST': 'localhost',
        'PORT': '',
    },
    'default_prod_pal': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waybill',
        'USER': 'root',
        'PASSWORD': 'epic',
        'HOST': 'localhost',
        'PORT': '',
    },
}

DATABASES = {
    "default": ALL_DB['default'],
    "compas": ALL_DB["compas_test_pak"],
}

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', ugettext('English')),
)

USE_I18N = True
USE_L10N = True

TIME_ZONE = 'Europe/Rome'

STATIC_ROOT = os.path.join(EGG_ROOT, 'static')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(EGG_ROOT, 'media')

SERVE_STATIC = True

STATICFILES_FINDERS = (
  "django.contrib.staticfiles.finders.FileSystemFinder",
  "django.contrib.staticfiles.finders.AppDirectoriesFinder",
  "ets.finders.AppMediaDirectoriesFinder",
)

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jxb_km(q=efo^64b)@o09ii!1c1z&pzo(3r-o(np&$n8qphao3'

TEMPLATE_DIRS = ( 
    os.path.join( PROJECT_ROOT, 'templates' ),
)

STATICFILES_DIRS = (
    os.path.join( PROJECT_ROOT, 'static' ),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    
    'audit_log.middleware.UserLoggingMiddleware',
    
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'ets.urls'

INSTALLED_APPS = (

    #own
    #'ets',
    'ets.waybill',
    
    # builtin
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.databrowse',
    'django.contrib.staticfiles',
    
    #external
    'django_extensions',
    #'ajax_select',
    #'uni_form',
    #'endless_pagination',
    #'sorl.thumbnail',
    #'tabs',
    #'mptt',
    'south',
    #'oembed',
    #'oembed.contrib',
    #'mailer',
    #'autoslug',
    #'native_tags',
    'rosetta',
    #'django_countries',
    'debug_toolbar',
    #'logicaldelete',
    #'floppyforms',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'ets.waybill.context_processor.common'
)

TEST_RUNNER = "ets.tests.coverage_runner.run_tests"
COVERAGE_REPORT_PATH = os.path.join(EGG_ROOT, 'coverage_report')

LOGIN_REDIRECT_URL = '/'
#=======================================================================================================================
# LOGIN_URL = '/account/login/'
# LOGOUT_URL = '/account/logout/'
#=======================================================================================================================
LOGIN_URL = '/test/ets/accounts/login/'
LOGOUT_URL = '/test/ets/accounts/logout/'
AUTH_PROFILE_MODULE = 'waybill.UserProfile'

IN_PRODUCTION = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = 'ets-demo'

WAYBILL_LETTER = 'A'
MAX_DATE = '2010-01-01'

SITE_NAME = ugettext('ETS')
DEFAULT_FROM_EMAIL = 'no-reply@wfp.com'
EMAIL_SUBJECT_PREFIX = ugettext("[ETS] ")
FEEDBACK_EMAIL = 'support@wfp.com'
#EMAIL_BACKEND = "mailer.backend.DbBackend"
SERVER_EMAIL = 'no-reply@wfp.com'

# debug toolbar
INTERNAL_IPS = ('127.0.0.1', )
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

COMPAS_STATION = u'JERX001'

# Local settings for development / production
try:
    from local import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DISABLE_EXPIERED_LTI = DEBUG



#testing to push again

#=======================================================================================================================
# INTSTANCE_LABLE = 'Toby Mac Pro'
#=======================================================================================================================
