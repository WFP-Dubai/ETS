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
from django.contrib.auth.models import User
from django.core import serializers




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
	profile=request.user.get_profile()
	return render_to_response('selectAction.html',
                              {'profile':profile},
                              context_instance=RequestContext(request))

def listOfLtis(request,origin):
    ltis = ltioriginal.objects.ltiCodesByWH(origin)
    profile=request.user.get_profile()
    wh_list =[]
    for wh in profile.warehouses.all():
    	wh_list += wh.ORIGIN_WH_CODE
    	
    print wh_list
    return render_to_response('ltis.html',
                              {'ltis':ltis,'profile':profile},
                              context_instance=RequestContext(request))

def ltis(request,origin):
    ltis = ltioriginal.objects.filter(ORIGIN_WH_CODE=origin).filter(EXPIRY_DATE__gt=datetime.date(2010, 4, 1))
    return render_to_response('ltis.html',
                              {'ltis':ltis},
                              context_instance=RequestContext(request))

def ltis_redirect_wh(request):
    wh_code = request.GET['dispatch_point']
    return HttpResponseRedirect('list/' + wh_code)


def import_ltis(request):
    #copy LTIs
    original = ltioriginal.objects.filter(LTI_DATE__year=2010).using('compas')
    for myrecord in original:
        myrecord.save(using='default')
    #Copy Persons
    originalPerson = EpicPerson.objects.using('compas')
    for myrecord in originalPerson:
        myrecord.save(using='default')    
    #Copy Stock
    originalStock = EpicStock.objects.using('compas')    
    for myrecord in originalStock:
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
    profile=request.user.get_profile()
    return render_to_response('dispatch_list.html',
                              {'dispatch_list':dispatch_list,'profile':profile},
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
                              
def waybill_view(request,wb_id):
	waybill_instance = Waybill.objects.get(id=wb_id)
	lti_detail_items = ltioriginal.objects.filter(CODE=waybill_instance.ltiNumber)
	return render_to_response('waybill/waybill_detail_view.html',
                              {'object':waybill_instance,
                              'ltioriginal':lti_detail_items},
                              context_instance=RequestContext(request))

def waybill_reception(request,wb_code):
	# get the LTI info
	current_wb = Waybill.objects.get(id=wb_code)
	current_lti = current_wb.ltiNumber
	class LoadingDetailDispatchForm(ModelForm):
		#siNo= ModelChoiceField(queryset=ltioriginal.objects.filter(CODE = lti_code),label='Commodity')
		
		class Meta:
			model = LoadingDetail
			fields = ('wbNumber','siNo','numberUnitsLoaded','numberUnitsGood','numberUnitsLost','numberUnitsDamaged','unitsLostReason','unitsDamagedReason',)

	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailDispatchForm,fk_name="wbNumber",  extra=1)
	if request.method == 'POST':
		formset = LDFormSet(request.POST)
	
		form = WaybillRecieptForm(request.POST)
		
		
		if form.is_valid() and formset.is_valid():
			wb_new = form.save()
			instances =formset.save(commit=False)
			for subform in instances:
				subform.wbNumber = wb_new
				subform.save()
			wb_new.save()
		
	else:
		form = WaybillRecieptForm(instance=current_wb)
		formset = LDFormSet(instance=current_wb)
	return render_to_response('recieveWaybill.html', 
			{'form': form,'lti_list':current_lti,'formset':formset},
			context_instance=RequestContext(request))
#    return render_to_response('recieveWaybill.html',                          {'status':'to be implemented'},                              context_instance=RequestContext(request))

def waybill_reception_list(request):
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


def waybillCreate(request,lti_code):
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
			return HttpResponseRedirect('../viewwb/'+ str(wb_new.id)) #
	else:
		form = WaybillForm(
			initial={
					'ltiNumber':         current_lti[0].CODE,
					'dateOfLoading':     datetime.date.today(),
					'dateOfDispatch':    datetime.date.today(),
					'dispatcherName':    request.user.get_full_name(),
					'recipientLocation': current_lti[0].DESTINATION_LOC_NAME
				}
		)
		formset = LDFormSet()
	return render_to_response('form.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))




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
			return HttpResponseRedirect('../viewwb/'+ str(wb_new.id)) # Redirect after POST
	else:
		form = WaybillForm(initial={'ltiNumber': current_lti[0].CODE})
		formset = LDFormSet()
	return render_to_response('form.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))
    

def serialize(request,wb_code):
	waybill_to_serialize = Waybill.objects.filter(id=wb_code)
	items_to_serialize = waybill_to_serialize[0].loadingdetail_set.select_related()
	data = serializers.serialize('json',list(waybill_to_serialize)+list(items_to_serialize))
	return render_to_response('status.html',{'status':data},
                              context_instance=RequestContext(request))

def custom_show_toolbar(request):
    return True

def printlistitem(list,index):
    print list(1)