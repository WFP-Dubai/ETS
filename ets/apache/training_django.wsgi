import os
import sys
sys.path.append('c:\\epic\\training\\')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ets.settings_training'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()