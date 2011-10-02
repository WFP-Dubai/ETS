
from django.contrib import admin

from .models import UpdateLog


class LoggerAdmin(admin.ModelAdmin):
    
    list_display = ('pk', 'date')
    date_hierarchy = 'date'

admin.site.register(UpdateLog, LoggerAdmin)
