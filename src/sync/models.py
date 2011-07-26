### -*- coding: utf-8 -*- ####################################################

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class ApiAction(models.Model):
    
    CREATE = 1
    UPDATE = 2
    
    ACTION_CHOICE = (
        (CREATE, _("Create")),
        (UPDATE, _("Update")),
    )
    
    type = models.IntegerField(_("type of action"), choices=ACTION_CHOICE)
    data = models.TextField(_("Serialized data"))
    created = models.DateTimeField(_("created date/time"), default=datetime.now)
    
    class Meta:
        ordering = ('created',)
        verbose_name=_("Postponed API action")
        verbose_name_plural = _("Postponed API actions")
