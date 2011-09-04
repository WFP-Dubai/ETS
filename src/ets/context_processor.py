from django.conf import settings # import the settings file


def common( context ):
    return {
        'IN_PRODUCTION': settings.IN_PRODUCTION,  
    }
