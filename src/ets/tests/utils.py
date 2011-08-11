### -*- coding: utf-8 -*- ####################################################

import os
from functools import wraps

from django.conf import settings

from windmill.authoring import djangotest


def change_settings(func, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        old_settings = {}
        for name, value in kwargs:
            old_settings[name] = getattr(settings, name)
            setattr(settings, value)
            
        result = func(*args, **kwargs)
        
        for name, value in kwargs:
            setattr(settings, old_settings[name])
        
        return result
    
    return wrapper


class WindmillMixin(object):
    def setUp(self):
        super(WindmillMixin, self).setUp()
        self.server_thread.fixtures = self.fixtures



def build_windmill_cases(app, path='tests/windmilltests',
                         browsers=getattr(settings, "WINDMILL_BROWSERS", ('firefox',)),
                         fixtures=()):
    """
        Generator, that returns test cases for every windmill suite and for every browser.
        based on http://www.rfk.id.au/blog/entry/django-unittest-windmill-goodness
        Author: Ryan Kelly
    """
    wmtests = os.path.join(os.path.dirname(os.path.abspath(app.__file__)), path)
    for test_module_name in os.listdir(wmtests):
        if test_module_name.startswith("test") and test_module_name.endswith(".py"):
            testnm = test_module_name[:-3]
            for cur_browser in browsers:
                name = "%s__%s" % (testnm, cur_browser)
                yield name, type(name,
                           (WindmillMixin, djangotest.WindmillDjangoUnitTest,),
                           {
                            'test_dir': os.path.join(wmtests, test_module_name),
                            'browser': cur_browser,
                            'fixtures': fixtures,
                           }
                        )
