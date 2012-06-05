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
from django.template.response import TemplateResponse
from django.utils.translation import ugettext
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from ajax_select import make_ajax_form
import logicaldelete.admin
from django_extensions.utils.text import truncate_letters

import ets.models
import ets.forms
from ets.utils import get_user_actions


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
            return u'<a href="../../%s/%s/%s">%s</a>' % (
                target._meta.app_label, target._meta.module_name, target.pk, unicode(target))

        for col in new_class.list_display:
            if col[:8] == 'link_to_':
                field_name = col[8:]
                method = partial(foreign_key_link, field=field_name)
                method.__name__ = col[8:]
                method.allow_tags = True
                method.admin_order_field = field_name
                setattr(new_class, col, method)

        return new_class


class CompasLoggerInline(admin.TabularInline):
    model = ets.models.CompasLogger
    extra = 0
    max_num = 5
    readonly_fields = ('action', 'compas', 'waybill', 'when_attempted', 'status', 'message')

class WaybillInline(admin.TabularInline):
    model = ets.models.Waybill
    extra = 0

class LoadingDetailsInline(admin.TabularInline):
    model = ets.models.LoadingDetail
    extra = 0
    raw_id_fields = ('waybill', 'stock_item')
    

class WaybillAdmin(logicaldelete.admin.ModelAdmin):
    __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass
    
    fieldsets = (
        (_('General'), {'fields': ('order', 'destination', )}),
        (_('Types'), {'fields': ('transaction_type', 'transport_type')}),
        (_('Dispatch'), {'fields': ('loading_date', 'dispatch_date', 'dispatcher_person', 'dispatch_remarks')}),
        (_('Transport'), {'fields': ('transport_sub_contractor', 'transport_driver_name', 
                                   'transport_driver_licence', 'transport_vehicle_registration', 
                                   'transport_trailer_registration', 'transport_dispach_signed_date',)}),
        (_('Container 1'), {'fields': ('container_one_number', 'container_one_seal_number', 
                                       'container_one_remarks_dispatch', 'container_one_remarks_reciept')}),
        (_('Container 2'), {'fields': ('container_two_number', 'container_two_seal_number', 
                                       'container_two_remarks_dispatch', 'container_two_remarks_reciept')}),
        (_("Receipt"), {'fields': ('arrival_date', 'start_discharge_date', 
                                   'end_discharge_date', 'receipt_signed_date', 
                                   'receipt_person', 'distance', 'receipt_remarks',)}),
        (_("COMPAS"), {'fields': ('validated', 'sent_compas', 'receipt_validated', 'receipt_sent_compas')}),
        (_("Utility"), {'fields': ('date_created', 'date_modified', 'date_removed')}),
    )
    
    list_display = ('pk', 'link_to_order', 'date_created', 'dispatch_date',
                    'destination', 'active')
    readonly_fields = ('order','date_created', 'date_modified')
    date_hierarchy = 'date_created'
    list_filter = ('date_created',)
    raw_id_fields = ('destination','dispatcher_person',)
    search_fields = ('slug', 'order__pk',)
    inlines = (LoadingDetailsInline, CompasLoggerInline)
    
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register( ets.models.Waybill, WaybillAdmin )


class OrderItemInline(admin.TabularInline):
    model = ets.models.OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'warehouse', 'consignee', 'created', 'dispatch_date', 'expiry')
    readonly_fields = ('created', 'updated')
    list_filter = ('dispatch_date', 'origin_type')
    search_fields = ('code', 'origin_type', 'warehouse__pk', 
                     'warehouse__compas__pk', 'warehouse__location__pk', 'warehouse__organization__pk')
    raw_id_fields = ('warehouse', 'consignee', 'location')
    inlines = (OrderItemInline,)

admin.site.register( ets.models.Order, OrderAdmin )

class OrderInline(admin.TabularInline):
    model = ets.models.Order
    extra = 0
    

class StockAdmin(admin.ModelAdmin):
    list_display = ('si_code', 'warehouse', 'project_number', 'commodity', 'quality', 
                    'get_package', 'number_of_units')
    readonly_fields = ('updated',)
    raw_id_fields = ('warehouse',)
    list_filter = ('warehouse__compas',)
    search_fields = ('code', 'warehouse__code', 'warehouse__name', 'project_number', 'si_code', 'commodity__name', 'package__name', 'si_record_id', 'origin_id')
    inlines = (LoadingDetailsInline,)
    
    def get_package(self, obj):
        return '<span title="%s">%s</span>' % (obj.package.name, truncate_letters(obj.package.name, 20))
    get_package.short_description = 'Package'
    get_package.allow_tags = True
    get_package.admin_order_field = 'package__name'
    
admin.site.register( ets.models.StockItem, StockAdmin )

class StockInline(admin.TabularInline):
    model = ets.models.StockItem
    extra = 0
    readonly_fields = ('warehouse','commodity','package')

class PersonInline(admin.TabularInline):
    model = ets.models.Person
    extra = 0
    readonly_fields = ('last_login', 'date_joined', 'compas', 'organization', 'location', 'code','warehouses','user_permissions')

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'organization', 'location', 'compas', 'start_date', 'end_date')
    list_editable = ('start_date',)
    list_filter = ('start_date', 'compas',)
    raw_id_fields = ('location', 'organization')
    search_fields = ('code', 'name', 'location__name', 'organization__name', 'compas__code')
    inlines = (StockInline,)
    
    def queryset(self, request):
        queryset = super(WarehouseAdmin, self).queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(compas__officers=request.user)
        return queryset
    
admin.site.register( ets.models.Warehouse, WarehouseAdmin )


class WarehouseInline(admin.TabularInline):
    model = ets.models.Warehouse
    raw_id_fields = ('location', 'organization')
    readonly_fields = ( 'name', 'organization', 'location', 'compas', 'start_date', 'end_date')
    extra = 0

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)
    inlines = (WarehouseInline, PersonInline,)

admin.site.register( ets.models.Organization, OrganizationAdmin )

class LocationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'country',)
    search_fields = ('code', 'name', 'country',)
    inlines = (WarehouseInline,)
    list_filter = ('country',)

admin.site.register( ets.models.Location, LocationAdmin )


class CompasAdmin(logicaldelete.admin.ModelAdmin):
    
    list_display = ('pk', 'read_only', 'active')
    search_fields = list_display
    list_filter = ('read_only',)
    filter_horizontal = ('officers',)
    fieldsets = (
        (_('General'), {'fields': ('code', 'read_only', 'officers')}),
        (_('Database'), {'fields': ('db_engine', 'db_name', 'db_user', 'db_password', 'db_host', 'db_port' )}),
        (_('Dates'), {'fields': ('date_created', 'date_modified', 'date_removed',)}),
    )
    actions = None

admin.site.register( ets.models.Compas, CompasAdmin )


class PackageAdmin( admin.ModelAdmin ):
    list_display = ('code', 'name',)
    search_fields = list_display

admin.site.register( ets.models.Package, PackageAdmin )

class LossDamageTypeAdmin(admin.ModelAdmin):
    __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass
    
    list_display = ('pk', 'type', 'link_to_category', 'cause')
    list_filter = ('type',)

admin.site.register( ets.models.LossDamageType, LossDamageTypeAdmin )


class CommodityAdmin(admin.ModelAdmin):
    __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass
    
    list_display = ('pk', 'name', 'link_to_category',)
    search_fields = ('name', 'category__pk')
    inlines = (StockInline,)

admin.site.register( ets.models.Commodity, CommodityAdmin )


class CommodityInline(admin.TabularInline):
    model = ets.models.Commodity
    extra = 0
    
class LossDamageTypeInline(admin.TabularInline):
    model = ets.models.LossDamageType
    extra = 0


class CommodityCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    search_fields = list_display
    inlines = (LossDamageTypeInline, CommodityInline)

admin.site.register( ets.models.CommodityCategory, CommodityCategoryAdmin )


class PersonAdmin(UserAdmin):
    __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass
    
    fieldsets = (
        (None, {'fields': ('username', 'compas', 'code', 'organization', 'location', 'warehouses', 'is_active',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'title')}),
        (_('Actions'), {'fields': ('dispatch', 'receive')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'username', 'code', 'title', 'get_full_name', 'link_to_compas', 
        'link_to_organization', 'link_to_location', 'dispatch', 'receive', 'is_active'
    )
    list_editable = ('is_active', 'dispatch', 'receive')
    list_filter = ('is_active', 'compas')
    search_fields = (
        'code', 'title', 'username', 'first_name', 'last_name', 'email',
        'compas__code', 'organization__name', 'organization__code', 'location__name'
    )
    readonly_fields = ('last_login', 'date_joined', 'compas', 'organization', 'location', 'code')
    raw_id_fields = ('organization', 'location')
    #filter_horizontal = ('warehouses',)
    form = make_ajax_form(ets.models.Person, dict(warehouses='warehouses'), ets.forms.PersonChangeForm)

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urls = super(PersonAdmin, self).get_urls()
        urls = patterns('',
                    url(r'^waybill-history/(?P<object_id>\d+)/$', self.admin_site.admin_view(self.waybill_history_view),
                        name="waybill_history")
                ) + urls
        return urls
    
    def queryset(self, request):
        queryset = super(PersonAdmin, self).queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(compas__officers=request.user)
        return queryset

    def waybill_history_view(self, request, object_id, template='admin/ets/person/waybill_history.html'):
        obj = self.get_object(request, admin.util.unquote(object_id))
        history_list = ets.models.ETSLogEntry.objects.filter(content_type__id=ContentType.objects.get_for_model(ets.models.Waybill).pk, user=obj)

        form = ets.forms.WaybillActionForm(request.POST or None)
        if form.is_valid() and form.cleaned_data['action_type']:
            history_list = history_list.filter(action_flag=form.cleaned_data['action_type'])
            
        context = {
            'history_list': history_list,
            'opts': self.opts,
            'title': 'Waybill history for user %s' % obj,
            'form': form,
            'person': obj,
            'paginate_by': getattr(settings, "WAYBILL_HISTORY_PAGINATE", 40)
        }
        return TemplateResponse(request, template, context)
    
admin.site.register(ets.models.Person, PersonAdmin)


class CompasLoggerAdmin(admin.ModelAdmin):
    __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass
    
    list_display = ('pk', 'action', 'link_to_compas', 'link_to_waybill', 'when_attempted', 'status', 'message')
    search_fields = ('compas__pk', 'waybill__pk')
    date_hierarchy = 'when_attempted'
    raw_id_fields = ('waybill',)
    list_filter = ('when_attempted', 'status', 'action', 'compas')

admin.site.register(ets.models.CompasLogger, CompasLoggerAdmin)


class ImportLoggerAdmin(admin.ModelAdmin):
    __metaclass__ = ModelAdminWithForeignKeyLinksMetaclass
    
    list_display = ('pk', 'link_to_compas', 'when_attempted', 'status', 'message')
    search_fields = ('compas__pk', 'message')
    date_hierarchy = 'when_attempted'
    list_filter = ('when_attempted', 'status', 'compas')

admin.site.register(ets.models.ImportLogger, ImportLoggerAdmin)


class LoggedUserAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [PersonInline,]

#admin.site.unregister(User)
#admin.site.register(User, PersonedUserAdmin)
