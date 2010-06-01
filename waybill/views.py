# Create your views here.
from django.template import Template, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from ets.waybill.models import *
from django.shortcuts import render_to_response
import datetime
from django.contrib.auth.views import login,logout
from django.contrib.auth.decorators import login_required

def prep_req(request):
    return{'user': request.user}
    
def hello(request):
    return HttpResponse("Hello World")

def homepage(request):
    return render_to_response('homepage.html',
                              {'status':'',},
                              context_instance=RequestContext(request))

def loginWaybillSystem(request):
    return render_to_response('status.html',
                              {'status':'login not yet implemented'},
                              context_instance=RequestContext(request))
    
def selectAction(request):
    return render_to_response('selectAction.html',
                              {'status':' selectAction not yet implemented'},
                              context_instance=RequestContext(request))

def listOfLtis(request,origin):
    ltis = ltioriginal.objects.filter(ORIGIN_LOCATION_CODE=origin)#.order_by('SI_CODE','CODE')
    return render_to_response('ltis.html',
                              {'ltis':ltis},
                              context_instance=RequestContext(request))

def ltis(request,origin):
    ltis = ltioriginal.objects.filter(ORIGIN_LOCATION_CODE=origin).filter(EXPIRY_DATE__gt=datetime.date(2010, 4, 1))
    return render_to_response('ltis.html',
                              {'ltis':ltis},
                              context_instance=RequestContext(request))
    
def ltis_redirect_wh(request):
    wh_code = request.GET['dispatch_point']
    return HttpResponseRedirect('list/' + wh_code)


def import_ltis(request):
    original = ltioriginal.objects.filter(LTI_DATE__year=2010).using('compas')
    for myrecord in original:
        myrecord.save(using='default')
    status = 'done'
    return render_to_response('status.html',
                              {'status':status},
                              context_instance=RequestContext(request))

def lti_detail(request):
    lti_id=request.GET['lti_id']
    #option here to redirect///
    return HttpResponseRedirect('info/' + lti_id)
    #return lti_detail_url(request,lti_id)

def lti_detail_url(request,lti_id):
    detailed_lti = ltioriginal.objects.filter(LTI_ID=lti_id)
    return render_to_response('detailed_lti.html',
                              {'detailed':detailed_lti,'lti_id':lti_id},
                              context_instance=RequestContext(request))
  

def dispatch(request):
    dispatch_list = ltioriginal.objects.warehouses()
    return render_to_response('dispatch_list.html',
                              {'dispatch_list':dispatch_list},
                              context_instance=RequestContext(request))
def ltis_codes(request):
	lti_codes = ltioriginal.objects.ltiCodes()
	return render_to_response('lti_list.html',
                              {'dispatch_list':lti_codes},
                              context_instance=RequestContext(request))
	
#### Waybill Views

def waybill_info(request):
        return render_to_response('status.html',
                              {'status':'to be implemented'},
                              context_instance=RequestContext(request))

def waybill_create(request,lti_pk):
    detailed_lti = ltioriginal.objects.get(LTI_PK=lti_pk)
    return render_to_response('detailed_waybill.html',
                              {'detailed':detailed_lti,'lti_id':lti_pk},
                              context_instance=RequestContext(request))

def waybill_edit(request):
	return render_to_response('status.html',
                              {'status':'to be implemented'},
                              context_instance=RequestContext(request))

def waybill_reception(request):
    return render_to_response('status.html',
                              {'status':'to be implemented'},
                              context_instance=RequestContext(request))
def waybill_search(request):
    return render_to_response('status.html',
                              {'status':'to be implemented'},
                              context_instance=RequestContext(request))

def waybillSearchResult(request):
    return render_to_response('status.html',
                              {'status':'selectAction not yet implemented'},
                              context_instance=RequestContext(request))

def waybill_validate_list(request):
    return render_to_response('status.html',
                              {'status':'to be implemented'},
                              context_instance=RequestContext(request))
def testform(request):	
	if request.method == 'POST':
		form = WaybillForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/thanks/')
	else:
		form = WaybillForm()
	return render_to_response('form.html', {'form': form,}, context_instance=RequestContext(request))
    
def custom_show_toolbar(request):
    return True

def printlistitem(list,index):
    print list(1)