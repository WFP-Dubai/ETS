# Django settings for ets project.

# This module is available as common_settings from projects' settings module.
# It contains settings used in all projects.

import os.path
from django.conf import global_settings

EGG_ROOT = os.path.abspath( os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../') )

ugettext = lambda s: s

DEBUG = False

MANAGERS = ( 
    # ('Your Name', 'your_email@domain.com'),
 )
ADMINS = ( 
    # ('Your Name', 'your_email@domain.com'),
 )

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', ugettext('English')),
)

USE_I18N = True
USE_L10N = False

TIME_ZONE = 'Europe/London'

STATIC_ROOT = os.path.join(EGG_ROOT, 'static')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(EGG_ROOT, 'media')

SERVE_STATIC = True

SERVE_STATIC = True

DEFAULT_FILE_STORAGE = 'ets.storage.RewriteFileSystemStorage'

STATICFILES_FINDERS = (
  "django.contrib.staticfiles.finders.FileSystemFinder",
  "django.contrib.staticfiles.finders.AppDirectoriesFinder",
  "ets.finders.AppMediaDirectoriesFinder",
  "compressor.finders.CompressorFinder",
)

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jxb_km(q=efo^64b)@o09ii!1c1z&pzo(3r-o(np&$n8qphao3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'ets.middleware.RequiredAuthenticationMiddleware',
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'ets.urls'

INSTALLED_APPS = (
    
    'south',
    
    'ets',
    'compas',
    
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.databrowse',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'django.contrib.humanize',
    
    'django_extensions',
    'rosetta',
    'debug_toolbar',
    'piston',
    'autoslug',
    'uni_form',
    'logicaldelete',
    'ajax_select',
    'native_tags',
    'compressor',
    'google_analytics',
    'pagination',
    'sorl.thumbnail',
    'concurrent_server',
    'clear_cache'
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
)

TEST_RUNNER = 'ets.tests.coverage_runner.CaverageTestSuiteRunner'
COVERAGE_REPORT_PATH = os.path.join(EGG_ROOT, 'coverage_report')

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = 'ets'
SESSION_COOKIE_AGE = 15 * 60 # 30 minutes age of cookie

WAYBILL_LETTER = 'A'

WAYBILL_HISTORY_PAGINATE = 40

SITE_NAME = ugettext('ETS')
DEFAULT_FROM_EMAIL = 'no-reply@wfp.com'
EMAIL_SUBJECT_PREFIX = ugettext("[ETS] ")
FEEDBACK_EMAIL = 'support@wfp.com'
#EMAIL_BACKEND = "mailer.backend.DbBackend"
SERVER_EMAIL = 'no-reply@wfp.com'

# debug toolbar
INTERNAL_IPS = ('127.0.0.1', )

DATE_FORMAT = "d-b-Y"
DATETIME_FORMAT = "d-b-Y H:i"

ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'

PAGINATION_DEFAULT_PAGINATION = 40

#Default life time of order (months)
DEFAULT_ORDER_LIFE = 3
ORDER_SHOW_AFTER_EXP_DAYS=30
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
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(EGG_ROOT, 'access.log')  # log file
        },
    },
    'loggers': {
        'django.request':{
            'handlers': ['console', 'mail_admins'],
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

# native tags
DJANGO_BUILTIN_TAGS = (
    'native_tags.templatetags.native',
)
NATIVE_TAGS = ()

THUMBNAIL_UPSCALE = True
THUMBNAIL_QUALITY = 98
THUMBNAIL_DEBUG = True
THUMBNAIL_FORMAT = 'JPEG'

#Loading details settings
LOADING_LINES = 5

AJAX_LOOKUP_CHANNELS = {
    #'warehouses': dict(model='ets.Warehouse', search_field='code'),
    'warehouses': ('ets.lookup', 'WarehouseChannel'),
}

AJAX_SELECT_INLINES = 'inline'
AJAX_SELECT_BOOTSTRAP = True

LOG_DIRECTORY = os.path.join(EGG_ROOT, 'logs') 
ALLOWED_INCLUDE_ROOTS = (LOG_DIRECTORY,)

class DatabasesFormDatabase(object):
    
    default = 'default'
    
    def __init__(self, default):
        super(DatabasesFormDatabase, self).__init__()
        self.default_db = default
    
    def get_compases(self):
        try:
            #Check applications aren't initialized yet
            from django.db.models.loading import get_model
            Compas = get_model(app_label='ets', model_name='Compas')
        except ImportError:
            return ()
        else:
            return Compas.objects.using(self.default)
    
    def __getitem__(self, alias):
        if alias != self.default:
            compas = self.get_compases().get(pk=alias)
            return {
                'NAME': compas.db_name,
                'ENGINE': compas.db_engine,
                'USER': compas.db_user,
                'PASSWORD': compas.db_password,
                'HOST': compas.db_host,
                'PORT': compas.db_port,
                'OPTIONS': {},
                'TEST_CHARSET': None,
                'TEST_COLLATION': None,
                'TEST_NAME': None,
                'TEST_MIRROR': None,
                'TIME_ZONE': TIME_ZONE
            }
        else:
            return self.default_db
    
    def items(self):
        return ( (self.default, self.default_db), )
        
        #===============================================================================================================
        # for alias in self:
        #    yield alias, self[alias]
        #===============================================================================================================
    
    def __iter__(self):
        yield self.default
        for compas in self.get_compases():
            yield compas.pk


DEFAULT_DATABASE = {
    'NAME': os.path.join(EGG_ROOT, 'db'),
    'ENGINE': 'django.db.backends.sqlite3',
    'USER': '',
    'PASSWORD': '',
    'HOST': 'localhost',
}

#Prevent migrations during testing
SOUTH_TESTS_MIGRATE = False

DEBUG = False
COMPRESS_ENABLED = True

# Local settings for development / production
try:
    from local_settings import *
except ImportError:
    pass

TEMPLATE_DEBUG = DEBUG
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'
DATABASES = DatabasesFormDatabase(DEFAULT_DATABASE)
SESSION_SAVE_EVERY_REQUEST = True
