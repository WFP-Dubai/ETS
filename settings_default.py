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
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'wb_pak',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'compas_test_pak': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.70.50/ISBX002',                	# Or path to database file if using sqlite3.
        'USER': 'TESTISBX002',                      	# Not used with sqlite3.
        'PASSWORD': 'TESTISBX002',                  		# Not used with sqlite3.
        'HOST': '10.11.70.50',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
    'default_tc_mb': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'waybill',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'compas_test_pal': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.216.4/JERX001',                	# Or path to database file if using sqlite3.
        'USER': 'TESTJERX001',                      	# Not used with sqlite3.
        'PASSWORD': 'TESTJERX001',                  		# Not used with sqlite3.
        'HOST': '10.11.216.4',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
       'default_tc_mp': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'waybill',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'compas_test_rome': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.33.199/tst1',                	# Or path to database file if using sqlite3.
        'USER': 'COMPAS_JERX001',                      	# Not used with sqlite3.
        'PASSWORD': 'JERX001',                  		# Not used with sqlite3.
        'HOST': '10.11.33.199',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
    'compas_prod_pal': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.216.4/JERX001',                	# Or path to database file if using sqlite3.
        'USER': 'opt_epic',                      	# Not used with sqlite3.
        'PASSWORD': 'opt_epic',                  		# Not used with sqlite3.
        'HOST': '10.11.33.199',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
        'default_serafino': {
        'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'waybill',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'postgres_password',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'offline_serafino': {
        'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'offline',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'postgres_password',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
        'default_training_pal': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'waybilltraining',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'epic',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	},
	'default_prod_pal': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'waybill',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'epic',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }

}
DATABASES = {
    'default': {},    
    'compas': {}
}


TIME_ZONE = 'Europe/Rome'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
ROOT_URLCONF = 'ets.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'ets.waybill',
    'django.contrib.databrowse',
#    'dojango',
    'debug_toolbar',
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
AUTH_PROFILE_MODULE='waybill.UserProfile'

TEMPLATE_CONTEXT_PROCESSORS =(
"django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.contrib.messages.context_processors.messages",
'django.core.context_processors.request'
)


COMPAS_STATION=u'JERX001'
INTSTANCE_LABLE="Toby Mac Pro"
LOGIN_URL = '/ets/accounts/login/'
LOGOUT_URL = '/ets/accounts/logout/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
EMAIL_HOST= 'docustore.wfp.org'
#EMAIL_USE_TLS=True