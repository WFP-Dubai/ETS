### -*- coding: utf-8 -*- ####################################################
"""
Configuration file used by setuptools. It creates 'egg', install all dependencies.

$Id$
"""

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#Dependencies - python eggs
install_requires = [
        'setuptools',
        'Django == 1.3',
        #'django-mailer', #asynchronous mail systembannerbs
#        'django-uni-form >= 0.7.0', #div-based forms
        #'django-endless-pagination',
        #'sorl-thumbnail',
        #'Pil',
        'httplib2',
        #'lxml == 2.2.6', 'BeautifulSoup',
#        'pytz',
#        'django-timezones',
        #'django-mptt >= 0.4.0',
        'south', #creates migrations
        #'tabs',
        #'django-countries',
        #'django-autoslug',
        #'pytils',
        #'django-native-tags==0.5.0',
        'django-rosetta',
        'django-extensions', #'python-keyczar', 'pyasn1',
        #'pygments',
        #'django-logicaldelete',
        #'pysolr',
        'django-debug-toolbar',
        #'pysolr',
        #'django-ajax-selects',
        'hashlib',
        #'django-floppyforms==0.4.5',
]

#Extra dependencies for test purposes
extras_require = dict(
    test=[
        'coverage', #checks code coverage by tests 
        #'windmill', #browser tests
    ]
)

#AFAIK:
install_requires.extend(extras_require['test'])

#List of paths, where parser may find packages
dependency_links = [
        'http://dist.plone.org/thirdparty/',
        'http://pypi.pinaxproject.com/',
        'http://dist.repoze.org',
#        'http://code.google.com/p/keyczar/downloads/list',
#        'http://code.google.com/p/django-ajax-selects/downloads/list',
]

#Execute function to handle setuptools functionality
setup(name="WFP-ETS",
            version="0.1",
            description="ETS",
            author="WFP",
            packages = ['ets'],
            include_package_data=True,
            zip_safe=False,
            install_requires=install_requires,
            extras_require=extras_require,
            entry_points="""
              # -*- Entry points: -*-
              """,
            dependency_links=dependency_links,
)
