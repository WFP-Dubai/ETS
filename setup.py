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
        #'httplib2',
        'south',
        'django-rosetta',
        'django-extensions', #'python-keyczar', 'pyasn1',
        'django-debug-toolbar',
        #'hashlib',
        'django-audit-log',
        #'cx_Oracle',
        'simplejson >= 2.1.0',
        'django-piston',
        'docutils',
        'django-autoslug',
        'django-uni-form >= 0.7.0', #div-based forms
        'django-logicaldelete',
        'django-native-tags==0.5.0',
]

#Extra dependencies for test purposes
extras_require = dict(
    test=[
        'coverage', #checks code coverage by tests 
        'windmill', #browser tests
    ]
)

#AFAIK:
install_requires.extend(extras_require['test'])

#List of paths, where parser may find packages
dependency_links = [
        'http://dist.plone.org/thirdparty/',
        'http://pypi.pinaxproject.com/',
        'http://dist.repoze.org',
        #'http://downloads.sourceforge.net/project/cx-oracle/5.1/cx_Oracle-5.1.tar.gz?r=http%3A%2F%2Fcx-oracle.sourceforge.net%2F&ts=1310462337&use_mirror=space',
]

#Execute function to handle setuptools functionality
setup(name="WFP-ETS",
            version="0.1",
            description="ETS",
            author="WFP",
            packages=find_packages('src'),
            package_dir={'': 'src'},
            include_package_data=True,
            zip_safe=False,
            install_requires=install_requires,
            extras_require=extras_require,
            entry_points="""
              # -*- Entry points: -*-
              """,
            dependency_links=dependency_links,
)
