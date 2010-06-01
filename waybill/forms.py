from django.forms import ModelForm
from ets.waybill.views import *

class WaybillForm(ModelForm):
     class Meta:
         model = Waybill

