# Create your views here.
import datetime
from django.contrib.auth.views import login,logout
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext
from ets.waybill.models import *
from ets.waybill.forms import *




def restant_si(lti_code):
	detailed_lti = ltioriginal.objects.filter(CODE=lti_code)
	listOfWaybills = Waybill.objects.filter(ltiNumber=lti_code)
	listOfSI = []
	for lti in detailed_lti:
		listOfSI += [SIWithRestant(lti.SI_CODE,lti.NUMBER_OF_UNITS,lti.CMMNAME)]
		
	for wb in listOfWaybills:
		for loading in wb.loadingdetail_set.select_related():
			for si in listOfSI:
				if si.SINumber == loading.siNo.SI_CODE:
					si.reduceCurrent(loading.numberUnitsLoaded)
					print 'x'

	return listOfSI
	

def prep_req(request):
    return{'user': request.user}

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
    ltis = ltioriginal.objects.ltiCodesByWH(origin)
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

def lti_detail_url(request,lti_code):
    detailed_lti = ltioriginal.objects.filter(CODE=lti_code)
    listOfWaybills = Waybill.objects.filter(ltiNumber=lti_code)
    listOfSI_withDeduction = restant_si(lti_code)
    
    return render_to_response('detailed_lti.html',
                              {'detailed':detailed_lti,'lti_id':lti_code,'listOfWaybills':listOfWaybills,'listOfSI_withDeduction':listOfSI_withDeduction},
                              context_instance=RequestContext(request))
def single_lti_extra(request,lti_code):
	si_list = ltioriginal.objects.si_for_lti(lti_code)
	return render_to_response('lti_si.html',
                              {'lti_code':lti_code,'si_list':si_list},
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



def testform(request,lti_code):
	# get the LTI info
	current_lti = ltioriginal.objects.filter(CODE = lti_code)
	lti_code_global = lti_code
	class LoadingDetailDispatchForm(ModelForm):
		siNo= ModelChoiceField(queryset=ltioriginal.objects.filter(CODE = lti_code),label='Commodity')
		
		class Meta:
			model = LoadingDetail
			fields = ('siNo','numberUnitsLoaded','wbNumber')
	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailDispatchForm,fk_name="wbNumber",  extra=5,max_num=5)

	if request.method == 'POST':
		form = WaybillForm(request.POST)
		formset = LDFormSet(request.POST)
		if form.is_valid() and formset.is_valid():
			wb_new = form.save()
			instances =formset.save(commit=False)
			for subform in instances:
				subform.wbNumber = wb_new
				subform.save()
			wb_new.save()
			
	else:
		form = WaybillForm(initial={'ltiNumber': current_lti[0].CODE})
		formset = LDFormSet()
		
	return render_to_response('form.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))
    
def custom_show_toolbar(request):
    return True

def printlistitem(list,index):
    print list(1)