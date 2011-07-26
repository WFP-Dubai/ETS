from django.contrib import admin

from .models import ApiAction


class ApiActionAdmin( admin.ModelAdmin ):
    list_display = ( 'pk', 'data', 'type', 'created' )
    list_filter = ( 'type', 'created' )
    date_hierarchy = 'created'
    ordering = ( '-created', )
    readonly_fields = ('created',)
    
admin.site.register( ApiAction, ApiActionAdmin )
