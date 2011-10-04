
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class ImportDataForm( forms.Form ):
    file = forms.FileField(required=True, label=_('Import Data'))

