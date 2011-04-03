from django.contrib import admin
from ets.waybill.models import *
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.admin import UserAdmin


class UserProfileInline( admin.StackedInline ):
    model = UserProfile
    verbose_name_plural = 'User Profile'

    def formfield_for_foreignkey( self, db_field, request, **kwargs ):
            if db_field.name == "warehouses":
                kwargs["queryset"] = DispatchPoint.objects.filter( ACTIVE_START_DATE__lte = datetime.date.today() )
            if db_field.name == "receptionPoints":
                kwargs["queryset"] = ReceptionPoint.objects.filter( ACTIVE_START_DATE__lte = datetime.date.today() )

            return super( UserProfileInline, self ).formfield_for_foreignkey( db_field, request, **kwargs )


class MyUserAdmin( UserAdmin ):
    list_display = ( 'username', 'first_name', 'last_name', 'email' )
    inlines = [UserProfileInline, ]
    fieldsets = [
    ( None, {'fields':[  'username', 'password', 'first_name', 'last_name', 'email']} ),
    ( 'Permissions', {'fields':[ 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'], 'classes': ['collapse']} ),
    ( 'Info', {'fields':['last_login', 'date_joined'], 'classes': ['collapse']} )
    ]
    def add_view( self, request, obj = None, **kwargs ):
        # hide every other field apart from url
        # if we are adding
        if obj is None:
            super( MyUserAdmin, self ).__setattr__( 'inline', None )
        return super( MyUserAdmin, self ).add_view( request, obj, **kwargs )


class EpicPersonsAdmin( admin.ModelAdmin ):
        list_display = ( 'last_name', 'first_name', 'title', 'location_code' )
        list_filter = ( 'location_code', 'organization_id' )


class LossesDamagesReasonAdmin( admin.ModelAdmin ):
        list_display = ( 'compasCode', 'description', 'compasRC' )
        list_filter = ( 'compasRC', )


class DispatchPointAdmin( admin.ModelAdmin ):
        list_display = ( 'origin_wh_name', 'origin_loc_name', 'origin_wh_code', 'ACTIVE_START_DATE' )
        ordering = ( 'ACTIVE_START_DATE', 'origin_loc_name', )
        list_filter = ( 'origin_loc_name', )
        readonly_fields = ( 'origin_loc_name', 'origin_wh_code', 'origin_location_code', )
        fieldsets = [
            ( 'Info', {'fields':['origin_loc_name', 'origin_wh_code', 'origin_location_code']} ),
            ( None, {'fields':['ACTIVE_START_DATE', 'origin_wh_name']} )
        ]


class ReceptionPointAdmin( admin.ModelAdmin ):
        list_display = ( 'LOC_NAME', 'consegnee_name', 'consegnee_code', 'ACTIVE_START_DATE' )
        ordering = ( 'ACTIVE_START_DATE', 'LOC_NAME', )
        list_filter = ( 'consegnee_name', 'LOC_NAME', )
        readonly_fields = ( 'LOC_NAME', 'consegnee_code', 'LOCATION_CODE', )
        fieldsets = [
            ( 'Info', {'fields':['LOC_NAME', 'consegnee_code', 'LOCATION_CODE']} ),
            ( None, {'fields':['ACTIVE_START_DATE', 'consegnee_name']} )
        ]

class UserProfileAdmin( admin.ModelAdmin ):
        list_display = ( 'user', 'warehouses', 'receptionPoints' )

        def formfield_for_foreignkey( self, db_field, request, **kwargs ):
            if db_field.name == "warehouses":
                kwargs["queryset"] = DispatchPoint.objects.filter( ACTIVE_START_DATE__lte = datetime.date.today() )
            if db_field.name == "receptionPoints":
                kwargs["queryset"] = ReceptionPoint.objects.filter( ACTIVE_START_DATE__lte = datetime.date.today() )

            return super( UserProfileAdmin, self ).formfield_for_foreignkey( db_field, request, **kwargs )



class PackagingDescriptonShortAdmin( admin.ModelAdmin ):
        list_display = ( 'packageCode', 'packageShortName' )
        list_filter = ( 'packageCode', 'packageShortName' )


class LoadingDetailAdmin( admin.ModelAdmin ):
        list_display = ( 'waybillNumber', 'siNo' )


admin.site.unregister( User )
admin.site.register( User, MyUserAdmin )
admin.site.register( UserProfile, UserProfileAdmin )
admin.site.register( DispatchPoint, DispatchPointAdmin )
admin.site.register( ReceptionPoint, ReceptionPointAdmin )
admin.site.register( EpicPerson, EpicPersonsAdmin )
admin.site.register( LossesDamagesReason, LossesDamagesReasonAdmin )
admin.site.register( LossesDamagesType )
admin.site.register( PackagingDescriptionShort, PackagingDescriptonShortAdmin )
admin.site.register( EpicLossReason )
