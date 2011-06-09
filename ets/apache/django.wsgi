import os
import sys
sys.path.append('c:\\epic')
sys.path.append('/Users/carlander/projects/epic/python_workspace/ets')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ets.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()