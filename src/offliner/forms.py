
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

UNDEFINED_MESSAGE = "N/A"

class ImportDataForm( forms.Form ):
    file = forms.CharField(required=True, label=_('Import Data'))

