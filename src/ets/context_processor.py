from django.conf import settings # import the settings file


def common( context ):
    return {
        'COMPAS_STATION': settings.COMPAS_STATION, 
        'IN_PRODUCTION': settings.IN_PRODUCTION,  
        'myprofile': context.user.is_authenticated() and context.user.get_profile()
    }
