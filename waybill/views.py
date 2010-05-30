# Create your views here.
from django.template import loader, Context, Template
from django.template.loader import get_template
from django.http import HttpResponse
from ets.waybill.models import EPIC_LTI, ltioriginal
import datetime

def hello(request):
    return HttpResponse("Hello World")
    
def ltis(request):
    now = ltioriginal.objects.using('compas').all()
    t = get_template('test.html')
    return HttpResponse(t.render(Context({'ltis':now})))
    #return loader.render_to_response('test.html',{'current_date':now})
    
    