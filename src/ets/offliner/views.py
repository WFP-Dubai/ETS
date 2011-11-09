
import datetime
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse
from django.core import serializers

from ..models import Warehouse, Waybill, LoadingDetail
from ..compress import compress_json, decompress_json

from .forms import ImportDataForm, ExportDataForm, DateRangeForm
from .models import UpdateLog

@login_required
def request_update(request):
    """requests data at server and import them localy"""
    last = None
    if UpdateLog.objects.count():
        last = UpdateLog.objects.latest("date")
    UpdateLog.request_data(last)

    return redirect('synchronization')

@require_POST
@login_required
def import_file(request, form_class=ImportDataForm):
    """Imports file with data."""    
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = form.cleaned_data['file']
        #File is supposed to be small (< 4Mb)
        UpdateLog.updata_data(file.read())
    return redirect('synchronization')

@require_GET
@login_required
def export_file(request, form_class=ExportDataForm):
    """exports file with data"""
    form = form_class(request.GET or None)
    if form.is_valid():
        warehouse = form.cleaned_data['warehouse']
        return redirect('api_offline', warehouse_pk=warehouse.pk)
    return redirect('synchronization')


@login_required
def export_waybills(request, template, form_class=DateRangeForm):
    """exports all offline waybills from selected period"""
    
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    
    form = form_class(request.POST or None, request.FILES or None, 
                      initial={'start_date': start_date, 'end_date': end_date})

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        waybills = Waybill.objects.filter(date_modified__range=(start_date, end_date+datetime.timedelta(1)))
        items = LoadingDetail.objects.filter(waybill__in=waybills)
        
        data = serializers.serialize('json', chain(waybills, items), use_decimal=False)
        #Cut field names
        data = compress_json(data)
        
        response = HttpResponse(data, content_type='application/json; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename=waybills-%s-%s.json' % (start_date, end_date)
        return response
    
    return direct_to_template(request, template, {
        'form': form,
    })

@login_required
def synchronization(request, template="synchronization.html", export_form=ExportDataForm, import_form=ImportDataForm):
    """
    Page for synchronization
    """
    export_form.base_fields['warehouse'].queryset = Warehouse.filter_by_user(request.user)
        
    return direct_to_template(request, template, {
        'form_import': import_form,
        'form_export': export_form,
    })

