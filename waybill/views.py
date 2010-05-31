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

def loginWaybillSystem(request):
    return render_to_response('status.html',{'status':'login not yet implemented'})
    
@login_required
def selectAction(request):
    return render_to_response('selectAction.html',{'status':' selectAction not yet implemented'})

def waybillSearchResult(request):
    return render_to_response('status.html',{'status':'selectAction not yet implemented'})    

def listOfLtis(request,origin):
    ltis = ltioriginal.objects.filter(ORIGIN_LOCATION_CODE=origin)#.order_by('SI_CODE','CODE')
    return render_to_response('ltis.html',{'ltis':ltis})

def ltis(request,origin):
    ltis = ltioriginal.objects.filter(ORIGIN_LOCATION_CODE=origin)#.order_by('SI_CODE','CODE')
    return render_to_response('ltis.html',{'ltis':ltis})
    
def ltis_redirect_wh(request):
    wh_code = request.GET['dispatch_point']
    return HttpResponseRedirect('list/' + wh_code)


def import_ltis(request):
    original = ltioriginal.objects.filter(LTI_DATE__year=2010).using('compas')
    for myrecord in original:
        myrecord.save(using='default')
    status = 'done'
    return render_to_response('status.html',{'status':status})

def lti_detail(request):
    lti_id=request.GET['lti_id']
    #option here to redirect///
    return HttpResponseRedirect('info/' + lti_id)
    #return lti_detail_url(request,lti_id)

def lti_detail_url(request,lti_id):
    detailed_lti = ltioriginal.objects.filter(LTI_ID=lti_id)
    return render_to_response('detailed_lti.html',{'detailed':detailed_lti,'lti_id':lti_id})

    

def dispatch(request):
    dispatch_list = ltioriginal.objects.warehouses()
    return render_to_response('dispatch_list.html',{'dispatch_list':dispatch_list})

    
def custom_show_toolbar(request):
    return True

def printlistitem(list,index):
    print list(1)