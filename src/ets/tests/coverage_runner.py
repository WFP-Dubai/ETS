### -*- coding: utf-8 -*- ####################################################
"""
=========   given from http://alarin.blogspot.com/ ===========
Test runner with code coverage.

"""

import os

from django.test import simple
from django.conf import settings

from coverage import coverage as Caverage

class CaverageTestSuiteRunner(simple.DjangoTestSuiteRunner):
    
    omit_folders = ('tests', 'settings', 'migrations')
    
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        coverage = Caverage()
        coverage.start()
        test_results = super(CaverageTestSuiteRunner, self).run_tests(test_labels, extra_tests=None, **kwargs)
        coverage.stop()

        if kwargs.get('verbosity', 1) >= 1:
            print "Generating coverage report..."

        coverage_modules = []
        for app in test_labels:
            try:
                module = __import__(app, globals(), locals(), [''])
            except ImportError:
                coverage_modules = None
                break
            if module:
                base_path = os.path.join(os.path.split(module.__file__)[0], "")
                for root, dirs, files in os.walk(base_path):
                    if not root.endswith(self.omit_folders):
                        for fname in files:
                            if fname.endswith(".py") and os.path.getsize(os.path.join(root, fname)) > 1:
                                try:
                                    mname = os.path.join(app, os.path.join(root, fname).replace(base_path, "")) 
                                    coverage_modules.append(mname)
                                except ImportError:
                                    pass #do nothing
        
        if coverage_modules or not test_labels:
            coverage.html_report(coverage_modules, directory=settings.COVERAGE_REPORT_PATH)
                    
        return test_results
