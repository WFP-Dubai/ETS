from django.contrib import admin
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#from django.utils.functional import curry
#from django.utils.translation import ugettext_lazy as _

import ets.models


class LoadingDetailsInline(admin.TabularInline):
    model = ets.models.LoadingDetail
    extra = 0

class WaybillAdmin(admin.ModelAdmin):
    #list_display = ('pk', 'status', 'ltiNumber', 'dateOfDispatch', 'dispatch_warehouse', 'destinationWarehouse')
    list_display = ('pk', 'status', 'order_code', 'dispatch_date', 'warehouse', 'destination')
    readonly_fields = ('created',)
    list_filter = ('status', 'created',)
    search_fields = ('pk',)
    inlines = (LoadingDetailsInline,)
    
admin.site.register( ets.models.Waybill, WaybillAdmin )


class OrderItemInline(admin.TabularInline):
    model = ets.models.OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'warehouse', 'consignee', 'created', 'dispatch_date', 'expiry')
    readonly_fields = ('created', 'updated')
    list_filter = ('dispatch_date', 'origin_type')
    search_fields = ('pk', 'origin_type', 'project_number')
    inlines = (OrderItemInline,)

admin.site.register( ets.models.Order, OrderAdmin )

class StockAdmin(admin.ModelAdmin):
    list_display = ('pk', 'warehouse', 'project_number', 'si_code', 'commodity_code', 
                    'package_code', 'number_of_units', 'quantity_net')
    readonly_fields = ('updated',)
    list_filter = ('warehouse',)
    search_fields = ('pk', 'warehouse__title', 'project_number', 'si_code', 'commodity_code', 'package_code',)

admin.site.register( ets.models.StockItem, StockAdmin )

class StockInline(admin.TabularInline):
    model = ets.models.StockItem
    extra = 0

class WarehouseAdmin(admin.ModelAdmin):
    #list_display = ('pk', 'title', 'place', 'start_date',)
    list_display = ('pk', 'name', 'location', 'start_date',)
    list_filter = ('location', 'start_date')
    #list_filter = ('place', 'start_date')
    date_hierarchy = 'start_date'
    search_fields = ('pk', 'title', 'place__name',)
    inlines = (StockInline,)
    
admin.site.register( ets.models.Warehouse, WarehouseAdmin )


class WarehouseInline(admin.TabularInline):
    model = ets.models.Warehouse
    extra = 0

class ConsigneeInline(admin.TabularInline):
    model = ets.models.Consignee
    extra = 0

class PersonInline(admin.TabularInline):
    model = ets.models.CompasPerson
    extra = 0

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'geo_point_code', 'geo_name', 'country_code', 'reporting_code',)
    list_filter = ('country_code',)
    search_fields = list_display
    inlines = (PersonInline, WarehouseInline, ConsigneeInline)
    
admin.site.register( ets.models.Place, PlaceAdmin )

class UserProfileInline( admin.StackedInline ):
    model = ets.models.UserProfile
    verbose_name_plural = 'User Profile'
    extra = 0


class UserAdmin( UserAdmin ):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PackagingDescriptonShortAdmin( admin.ModelAdmin ):
    list_display = ( 'code', 'description')
    #list_display = ( 'pk', 'description')
    list_filter = list_display

admin.site.register( ets.models.PackagingDescriptionShort, PackagingDescriptonShortAdmin )

class LossDamageTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type', 'comm_category_code', 'cause')
    list_filter = ('type',)

admin.site.register( ets.models.LossDamageType, LossDamageTypeAdmin )
