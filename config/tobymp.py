from datetime import *
# Django settings for ets project.
print 'Tobias Settings ' + str(datetime.today())
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'wbprod',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },    
    'compas': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.216.4/JERX001',                	# Or path to database file if using sqlite3.
        'USER': 'testjerx001',                      	# Not used with sqlite3.
        'PASSWORD': 'testjerx001',                  		# Not used with sqlite3.
        'HOST': '10.11.216.4',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    }#test opt
}

DATABASES_OTHER = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'wbprod',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'compasTestRome': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.33.199/tst1',                	# Or path to database file if using sqlite3.
        'USER': 'COMPAS_JERX001',                      	# Not used with sqlite3.
        'PASSWORD': 'JERX001',                  		# Not used with sqlite3.
        'HOST': '10.11.33.199',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
    
    'compasTestOTP': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.216.4/JERX001',                	# Or path to database file if using sqlite3.
        'USER': 'TESTJERX001',                      	# Not used with sqlite3.
        'PASSWORD': 'TESTJERX001',                  		# Not used with sqlite3.
        'HOST': '10.11.216.4',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
    'compasTest': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.216.4/JERX001',                	# Or path to database file if using sqlite3.
        'USER': 'opt_epic',                      	# Not used with sqlite3.
        'PASSWORD': 'opt_epic',                  		# Not used with sqlite3.
        'HOST': '10.11.33.199',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    },
    
    'compas': {
        'ENGINE': 'django.db.backends.oracle', 			# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '10.11.216.4/JERX001',                	# Or path to database file if using sqlite3.
        'USER': 'testjerx001',                      	# Not used with sqlite3.
        'PASSWORD': 'testjerx001',                  		# Not used with sqlite3.
        'HOST': '10.11.216.4',                     	# Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      				# Set to empty string for default. Not used with sqlite3.
    }#test opt
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jxb_km(q=efo^64b)@o09ii!1c1z&pzo(3r-o(np&$n8qphao3'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'audit_log.middleware.UserLoggingMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'ets.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'ets.waybill',
#    'dojango',
#    'debug_toolbar',
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
