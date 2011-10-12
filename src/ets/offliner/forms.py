
from django import forms
from django.utils.translation import ugettext_lazy as _

from ..models import Warehouse

class ImportDataForm( forms.Form ):
    file = forms.FileField(required=True, label=_('Import Data'))

class ExportDataForm( forms.Form ):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), required=True, label=_('Warehouse'))

