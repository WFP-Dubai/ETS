import os
import sys

sys.path.append('c:/epic/ets/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ets.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()