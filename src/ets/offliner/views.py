
import datetime
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse

from ..models import Warehouse, Waybill, LoadingDetail
from ..compress import compress_json, decompress_json

from .models import UpdateLog

@login_required
def request_update(request):
    """requests data at server and import them localy"""
    last = None
    if UpdateLog.objects.count():
        last = UpdateLog.objects.latest("date")
    UpdateLog.request_data(last)

    return redirect('synchronization')

#===============================================================================
# @login_required
# def synchronization(request, template="synchronization.html", export_form=ExportDataForm, import_form=ImportDataForm):
#    """
#    Page for synchronization
#    """
#    export_form.base_fields['warehouse'].queryset = Warehouse.objects.filter(persons__pk=request.user.pk)
#        
#    return direct_to_template(request, template, {
#        'form_import': import_form,
#        'form_export': export_form,
#    })
#===============================================================================
