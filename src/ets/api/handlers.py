### -*- coding: utf-8 -*- ####################################################

from datetime import datetime
from decimal import Decimal

from django.http import Http404
import httplib, logging

from piston.handler import BaseHandler

from cj.models import History


log = logging.getLogger(__name__)

date_format = '%Y-%m-%d'


class HistoryHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = History
    fields = (('user',("username",)), 'date', 'cash')
#    exclude = ('resource_uri',)

    def read(self, request):
        """
        Method **read** of **History** handler used to retrieve all History objects existing in database.
        It can be useful for initial database loading without any filtering.

        **URL** : */mall/api/history/*
        """
        return self.model.objects.all()

#    @staticmethod
#    def resource_uri(*args, **kwargs):
#        return ('history', [])


class HistoryIdHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = History
    fields = (('user',("username",)), 'date', 'cash')
#    exclude = ('resource_uri',)

    def read(self, request, object_id):
        """
        Method **read** of **HistoryIdHandler** handler used to retrieve History objects filtered by *object_id*.

        - *object_id* - ID of history object in database
        - *restrict* - optional argument of GET query. If present result set limits will be restricted. Argument value will not affect the result.

        When **restrict** argument of query provided then only one **History** object with ID equal to **object_id**
          will be returned otherwise method will fetch all **History** objects with with ID greater than **object_id** value.

        **URL** : */mall/api/history/id/{object_id}/*
        """
        restrict = 'restrict' in request.GET

        if restrict:
            return self.model.objects.filter(id=object_id)
        else:
            return self.model.objects.filter(id__gt=object_id)

#    @staticmethod
#    def resource_uri(*args, **kwargs):
#        return ('history_id', {'object_id':'id'})


    
class HistoryDateHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = History
    fields = (('user',("username",)), 'date', 'cash')
#    exclude = ('resource_uri',)

    def read(self, request, date):
        """
        Method **read** of **HistoryIdHandler** handler used to retrieve History objects filtered by *date* of event.

        - *date* - date/datetime of history object in database. Required date format is *%Y-%m-%d* (e.g 2011-06-20)
        - *restrict* - optional argument of GET query. If present result set limits will be restricted. Argument value will not affect the result.

        When **restrict** argument of query provided then only one **History** object with event date equal to **date**
          will be returned otherwise method will fetch all **History** objects with with event date later than **date** value.

        **URL** : */mall/api/history/date/{date}/*
        """
        date = datetime.strptime(date, date_format)
        restrict = 'restrict' in request.GET

        if restrict:
            return self.model.objects.filter(date__year=date.year, date__month=date.month, date__day=date.day)
        else:
            return self.model.objects.filter(date__gt=date)

#    @staticmethod
#    def resource_uri(*args, **kwargs):
#        return ('history_date', ['date',])


class HistoryUserHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = History
    fields = (('user',("username",)), 'date', 'cash')
#    exclude = ('resource_uri',)

    def read(self, request, username):
        """
        Method **read** of **HistoryIdHandler** handler used to retrieve History objects filtered by *username* of user.

        - *username* - user name who has earned commission for which history object stored in database

        **URL** : */mall/api/history/user/{username}/*

        """
        return self.model.objects.filter(user__username=username)

#    @staticmethod
#    def resource_uri(*args, **kwargs):
#        return ('history_user', {'username':'username'})