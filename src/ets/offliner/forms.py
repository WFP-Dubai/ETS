
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from uni_form.helper import FormHelper
from uni_form.layout import Layout, Fieldset, Row, Submit


class DateRangeForm(forms.Form):
    
    start_date = forms.DateField(label=_('Start date'))
    end_date = forms.DateField(label=_('End date'))
    
    helper = FormHelper()
    
    # create the layout object
    helper.add_layout(Layout(
        Fieldset(_('Select date range'), Row('start_date', 'end_date')),
    ))
    
    helper.add_input(Submit(_("Download"), 'download'))
