from django.conf import settings # import the settings file


def request( context ):
    users_profile = ''
    try:
        users_profile = context.user.profile
    except:
        pass
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'COMPAS_STATION':settings.COMPAS_STATION, 'IN_PRODUCTION':settings.IN_PRODUCTION, 'MEDIA_URL':settings.MEDIA_URL, 'myprofile':users_profile}
