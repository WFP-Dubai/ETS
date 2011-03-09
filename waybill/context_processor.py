from django.conf import settings # import the settings file


def request(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'COMPAS_STATION':settings.COMPAS_STATION,'PRODUCTION_SYSTEM':settings.IN_PROCDUCTION,'MEDIA_URL':settings.MEDIA_URL}
