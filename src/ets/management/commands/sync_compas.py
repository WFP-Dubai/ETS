### -*- coding: utf-8 -*- ####################################################

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Updates lti and stock.'

    requires_model_validation = False

    #@transaction.commit_on_success
    def handle(self, *args, **options):

        verbosity = int(options.get('verbosity', 1))
        if verbosity >= 2:
            print("Uploading data ...")

    