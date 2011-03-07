from django.contrib import admin
from ets.waybill.models import *
from django.contrib.auth.models import User


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline,
    ]

class EpicPersonsAdmin(admin.ModelAdmin):
        list_display = ('last_name','first_name','title' , 'location_code')
        list_filter = ( 'location_code','organization_id')


class LossesDamagesReasonAdmin(admin.ModelAdmin):
        list_display = ('compasCode','description','compasRC')
        list_filter = ('compasRC',) 

class DispatchPointAdmin(admin.ModelAdmin):
        list_display=('origin_wh_name','origin_loc_name','origin_wh_code')
        ordering = ('origin_loc_name',)
        list_filter = ('origin_loc_name',) 
        

class ReceptionPointAdmin(admin.ModelAdmin):
        list_display=('LOC_NAME','consegnee_name','consegnee_code')
        ordering = ('LOC_NAME',)
        list_filter = ('consegnee_name',) 
        
class UserProfileAdmin(admin.ModelAdmin):
        list_display=('user','warehouses')

class PackagingDescriptonShortAdmin(admin.ModelAdmin):
        list_display=('packageCode','packageShortName')
        list_filter = ('packageCode','packageShortName') 

class LoadingDetailAdmin(admin.ModelAdmin):
        list_display=('waybillNumber','siNo')

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(UserProfile)
admin.site.register(DispatchPoint,DispatchPointAdmin)
admin.site.register(ReceptionPoint,ReceptionPointAdmin)
admin.site.register(EpicPerson,EpicPersonsAdmin)
admin.site.register(LossesDamagesReason,LossesDamagesReasonAdmin)
admin.site.register(LossesDamagesType)
admin.site.register(PackagingDescriptonShort,PackagingDescriptonShortAdmin)
admin.site.register(EpicLossReason)
#admin.site.register(LoadingDetailAuditLogEntry)