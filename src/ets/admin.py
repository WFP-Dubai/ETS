import datetime
from functools import partial

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict
from django.http import HttpResponseRedirect
from django.forms import MediaDefiningClass

import logicaldelete.admin

import ets.models


class ButtonableModelAdmin(admin.ModelAdmin):

    buttons = ()

    def change_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, admin.util.unquote(object_id))
        extra = {'buttons': self.get_buttons(request, obj).values()}
        extra.update(extra_context or {})

        return super(ButtonableModelAdmin, self).change_view(request, object_id, extra_context=extra)

    def button_view_dispatcher(self, request, object_id, command):
        obj = self.get_object(request, admin.util.unquote(object_id))
        response = self.get_buttons(request, obj)[command][0](request, obj)

        return response or HttpResponseRedirect(request.META['HTTP_REFERER'])

    def get_buttons(self, request, obj):
        """
        Return a dictionary mapping the names of all buttons for this
        ModelAdmin to a tuple of (callable, name, description) for each button.
        Each button may assign 'condition', which chould be callable with following attrs: self, request, obj
        """

        buttons = SortedDict()
        for name in self.buttons:
            handler = getattr(self, name)
            if getattr(handler, 'condition', lambda self, request, obj: True)(self, request, obj):
                buttons[name] = (handler, name,
                                 getattr(handler, 'short_description', name.replace('_', ' ')))

        return buttons

    def get_urls(self):

        from django.conf.urls.defaults import patterns, url
        from django.utils.functional import update_wrapper

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        return patterns('',
            *(url(r'^(\d+)/(%s)/$' % command, wrap(self.button_view_dispatcher)) for command in self.buttons)
        ) + super(ButtonableModelAdmin, self).get_urls()


class ModelAdminWithForeignKeyLinksMetaclass(MediaDefiningClass):

    def __new__(cls, name, bases, attrs):
        new_class = super(ModelAdminWithForeignKeyLinksMetaclass, cls).__new__(cls, name, bases, attrs)

        def foreign_key_link(instance, field):
            target = getattr(instance, field)
            return u'<a href="../../%s/%s/%d">%s</a>' % (
                target._meta.app_label, target._meta.module_name, target.id, unicode(target))

        for col in new_class.list_display:
            if col[:8] == 'link_to_':
                field_name = col[8:]
                method = partial(foreign_key_link, field=field_name)
                method.__name__ = col[8:]
                method.allow_tags = True
                method.admin_order_field = field_name
                setattr(new_class, col, method)

        return new_class


class LoadingDetailsInline(admin.TabularInline):
    model = ets.models.LoadingDetail
    extra = 0
    
    fieldsets = (
        (_("Stock"), {'fields': ('stock_item',)}),
        (_('Loading details'), {'fields': ('number_of_units', 'overloaded_units')}),
        (_('Receipt details'), {'fields': ('number_units_good', 'number_units_lost', 'number_units_damaged', 
                                           'units_lost_reason', 'units_damaged_reason')}),
        (_('Utility information'), {'fields': ('sent_compas', 'over_offload_units')}),
    )
    
class ReceiptInline(admin.StackedInline):
    model = ets.models.ReceiptWaybill
    extra = 0
    
    fieldsets = (
        (_('Dates'), {'fields': ('arrival_date', 'start_discharge_date', 
                                 'end_discharge_date', 'signed_date',)}),
        (_("Reception details"), {'fields': ('person', 'distance', 'remarks',)}),
        (_('Containers'), {'fields': ('container_one_remarks_reciept', 'container_two_remarks_reciept',)}),
        (_("Utility information"), {'fields': ('validated', 'sent_compas')}),
    )

class WaybillAdmin(logicaldelete.admin.ModelAdmin):
    __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass
    
    fieldsets = (
        (_('General'), {'fields': ('order', 'destination', 'status',)}),
        (_('Types'), {'fields': ('transaction_type', 'transport_type')}),
        (_('Dispatch'), {'fields': ('loading_date', 'dispatch_date', 'dispatcher_person', 'dispatch_remarks')}),
        (_('Transport'), {'fields': ('transport_sub_contractor', 'transport_driver_name', 
                                   'transport_driver_licence', 'transport_vehicle_registration', 
                                   'transport_trailer_registration', 'transport_dispach_signed_date',)}),
        (_('Container 1'), {'fields': ('container_one_number', 'container_one_seal_number', 
                                       'container_one_remarks_dispatch',)}),
        (_('Container 2'), {'fields': ('container_two_number', 'container_two_seal_number', 
                                       'container_two_remarks_dispatch',)}),
        (_("COMPAS"), {'fields': ('validated', 'sent_compas',)}),
    )
    
    add_fieldsets = (
        (_('Order'), {'fields': ('order', 'destination')}),
        (_('Types'), {'fields': ('transaction_type', 'transport_type')}),
        (_('Dispatch'), {'fields': ('loading_date', 'dispatch_date', 'dispatcher_person', 'dispatch_remarks')}),
        (_('Transport'), {'fields': ('transport_sub_contractor', 'transport_driver_name', 
                                   'transport_driver_licence', 'transport_vehicle_registration', 
                                   'transport_trailer_registration', 'transport_dispach_signed_date',)}),
        (_('Container 1'), {'fields': ('container_one_number', 'container_one_seal_number', 
                                       'container_one_remarks_dispatch',)}),
        (_('Container 2'), {'fields': ('container_two_number', 'container_two_seal_number', 
                                       'container_two_remarks_dispatch',)}),
    )
    
    list_display = ('pk', 'status', 'link_to_order', 'date_created', 'dispatch_date', 
                    'destination', 'active')
    readonly_fields = ('date_created',)
    date_hierarchy = 'date_created'
    list_filter = ('status', 'date_created',)
    search_fields = ('pk', 'order__pk')
    inlines = (LoadingDetailsInline, ReceiptInline)
        
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)
    
    def get_formsets(self, request, obj=None):
        for inline in self.inline_instances:
            if obj or inline.model is not ets.models.ReceiptWaybill:
                yield inline.get_formset(request, obj)
    
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

class OrderInline(admin.TabularInline):
    model = ets.models.Order
    extra = 0
    

class StockAdmin(admin.ModelAdmin):
    list_display = ('pk', 'warehouse', 'project_number', 'si_code', 'comm_category_code', 'commodity_name', 
                    'package_name', 'number_of_units', 'unit_weight_net')
    readonly_fields = ('updated',)
    list_filter = ('warehouse',)
    search_fields = ('pk', 'warehouse__title', 'project_number', 'si_code', 'commodity_code', 'package_code',)

admin.site.register( ets.models.StockItem, StockAdmin )

class StockInline(admin.TabularInline):
    model = ets.models.StockItem
    extra = 0

class PersonInline(admin.TabularInline):
    model = ets.models.Person
    extra = 0

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'organization', 'location', 'compas', 'start_date',)
    list_filter = ('location', 'start_date')
    date_hierarchy = 'start_date'
    search_fields = ('pk', 'title', 'place__name',)
    inlines = (StockInline, OrderInline)
    
admin.site.register( ets.models.Warehouse, WarehouseAdmin )


class WarehouseInline(admin.TabularInline):
    model = ets.models.Warehouse
    extra = 0

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = list_display
    inlines = (PersonInline, WarehouseInline, OrderInline)

admin.site.register( ets.models.Organization, OrganizationAdmin )

class LocationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'country',)
    search_fields = list_display
    inlines = (WarehouseInline, OrderInline)
    list_filter = ('country',)

admin.site.register( ets.models.Location, LocationAdmin )


class CompasAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    search_fields = list_display
    inlines = (WarehouseInline, PersonInline)

admin.site.register( ets.models.Compas, CompasAdmin )


class PackagingDescriptonShortAdmin( admin.ModelAdmin ):
    list_display = ('code', 'description')
    list_filter = list_display

admin.site.register( ets.models.PackagingDescriptionShort, PackagingDescriptonShortAdmin )

class LossDamageTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type', 'comm_category_code', 'cause')
    list_filter = ('type',)

admin.site.register( ets.models.LossDamageType, LossDamageTypeAdmin )
