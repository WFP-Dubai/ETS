# Django settings for ets project.
print 'Settings Default'
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

ALL_DB = {
    'default_tc_pak': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wb_pak',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
    'default_test_pak': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waybill_pak',
        'USER': 'root',
        'PASSWORD': 'trackme',
        'HOST': 'localhost',
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
        'NAME': '10.11.33.199/tst1',
        'USER': 'COMPAS_JERX001',
        'PASSWORD': 'JERX001',
        'HOST': '10.11.33.199',
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
    }
}

DATABASES = {'default': {}, 'compas': {}}

TIME_ZONE = 'Europe/Rome'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'jxb_km(q=efo^64b)@o09ii!1c1z&pzo(3r-o(np&$n8qphao3'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'audit_log.middleware.UserLoggingMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
ROOT_URLCONF = 'ets.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'ets.waybill',
    'django.contrib.databrowse',
)
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
AUTH_PROFILE_MODULE = 'waybill.UserProfile'

TEMPLATE_CONTEXT_PROCESSORS = (
'django.contrib.auth.context_processors.auth',
'django.core.context_processors.debug',
'django.core.context_processors.i18n',
'django.contrib.messages.context_processors.messages',
'django.core.context_processors.request',
'ets.waybill.context_processor.request'
)

import os
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)

COMPAS_STATION = u'JERX001'
INTSTANCE_LABLE = 'Toby Mac Pro'
LOGIN_URL = '/ets/accounts/login/'
LOGOUT_URL = '/ets/accounts/logout/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
IN_PRODUCTION = False
SESSION_COOKIE_NAME = 'ets-demo'
