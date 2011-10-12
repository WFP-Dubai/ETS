
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
#from django.core import serializers
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.contrib import messages
from django.db import transaction
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST, require_GET

from .forms import ImportDataForm, ExportDataForm


from .models import UpdateLog

@login_required
def request_update(request):
    """requests data at server and import them localy"""    
    
    UpdateLog.request_data()
    
    return redirect('index')

@require_POST
@login_required
def import_file(request, form_class=ImportDataForm):
    """imports file with data"""    
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        file = form.cleaned_data['file']
        UpdateLog.updata_data(file.read())
    return redirect('index')

@require_GET
@login_required
def export_file(request, form_class=ExportDataForm):
    """exports file with data"""
    print 'KILL'
    form = form_class(request.GET or None)
    if form.is_valid():
        print "VALID"
        warehouse = form.cleaned_data['warehouse']
        print warehouse
        return redirect('api_offline', warehouse_pk=warehouse.pk)
    return redirect('index')
