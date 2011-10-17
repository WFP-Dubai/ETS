
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.simple import direct_to_template
from django.views.decorators.http import require_POST, require_GET

from ..models import Warehouse

from .forms import ImportDataForm, ExportDataForm
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
    """imports file with data"""    
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = form.cleaned_data['file']
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
def synchronization(request, template="synchronization.html", export_form=ExportDataForm, import_form=ImportDataForm):
    """
    Page for synchronization
    """
    export_form.base_fields['warehouse'].queryset = Warehouse.filter_by_user(request.user)
        
    return direct_to_template(request, template, {
        'form_import': import_form,
        'form_export': export_form,
    })

