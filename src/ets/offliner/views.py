
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from ets.utils import data_to_file_response

from ets.offliner.forms import DateRangeForm
from ets.offliner.models import UpdateLog
from ets.offliner.utils import compress_waybills

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

class ExportWaybillData(FormView):
    
    template_name = 'offliner/export_waybills.html'
    form_class = DateRangeForm
    file_name = 'waybills-%(start_date)s-%(end_date)s'
    
    def get_initial(self):
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)
        return {'start_date': start_date, 'end_date': end_date}
    
    def form_valid(self, form):
        start_date = form.cleaned_data['start_date'] 
        end_date = form.cleaned_data['end_date']
        
        data = compress_waybills(start_date, end_date)
        
        return data_to_file_response(data, self.file_name % {
            'start_date': start_date, 
            'end_date': end_date,
        })
