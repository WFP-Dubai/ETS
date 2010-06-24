# Create your views here.
import datetime
from django.contrib.auth.views import login,logout
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory,modelformset_factory

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
@login_required	
def selectAction(request):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	return render_to_response('selectAction.html',
							  {'profile':profile},
							  context_instance=RequestContext(request))

def listOfLtis(request,origin):
	ltis = ltioriginal.objects.ltiCodesByWH(origin)
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
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
	#Copy Persons
	originalPerson = EpicPerson.objects.using('compas').filter(org_unit_code='JERX001')
	for myrecord in originalPerson:
		myrecord.save(using='default')	
	#copy LTIs
	original = ltioriginal.objects.using('compas').filter(LTI_DATE__gt='2010-05-01')
	for myrecord in original:
		myrecord.save(using='default')
		mysist = SiTracker()
		mysist.LTI=myrecord
		mysist.number_units_left = myrecord.NUMBER_OF_UNITS
		try:
			mysist.save(using='default')
		except:
			pass
	#UPDATE GEO
#	try:
#	my_geo = GeoLocations.objects.using('compas').filter(COUNTRY_CODE='275')
#	for the_geo in my_geo:
#			if the_geo.COUNTRY_CODE == '275':
#   			the_geo.save(using='default')
#	except:
#		pass
   # my_geo = GeoLocations.objects.using('compas').filter(COUNTRY_CODE='376')
   # for the_geo in my_geo:
   # 	the.geo.save(using='default')
	
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
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
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
							  
							  
def waybill_finalize_dispatch(request,wb_id):
	current_wb =  Waybill.objects.get(id=wb_id)
	current_wb.transportDispachSigned=True
	current_wb.transportDispachSignedTimestamp=datetime.datetime.now()
	current_wb.dispatcherSigned=True
	for lineitem in current_wb.loadingdetail_set.select_related():
		print lineitem.numberUnitsLoaded
		print lineitem.siNo.restant()
		lineitem.siNo.reducesi(lineitem.numberUnitsLoaded)
	current_wb.save()
	return HttpResponseRedirect('/ets/waybill/dispatch') #
	
	
def	waybill_finalize_reciept(request,wb_id):
	current_wb =  Waybill.objects.get(id=wb_id)
	current_wb.recipientSigned=True
	current_wb.transportDeliverySignedTimestamp=datetime.datetime.now()
	current_wb.recipientSignedTimestamp=datetime.datetime.now()	
	current_wb.transportDeliverySigned=True
	current_wb.save()
	print 	current_wb.transportDeliverySigned
	return HttpResponseRedirect('/ets/waybill/viewwb_reception/' + str(current_wb.id)) #






def waybill_edit(request,wb_id):
	current_wb =  Waybill.objects.get(id=wb_id)
	lti_code = current_wb.ltiNumber
	current_lti = ltioriginal.objects.filter(CODE = lti_code)
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	class LoadingDetailDispatchForm(ModelForm):
		siNo= ModelChoiceField(queryset=ltioriginal.objects.filter(CODE = lti_code),label='Commodity')
		class Meta:
			model = LoadingDetail
			fields = ('siNo','numberUnitsLoaded','wbNumber')

	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailDispatchForm,fk_name="wbNumber",  extra=5,max_num=5)

	if request.method == 'POST':
		form = WaybillForm(request.POST,instance=current_wb)
		formset = LDFormSet(request.POST,instance=current_wb)
		if form.is_valid() and formset.is_valid():
			wb_new = form.save()
			instances =formset.save()
			return HttpResponseRedirect('../viewwb/'+ str(wb_new.id)) #
	else:			
		form = WaybillForm(instance=current_wb)
		formset = LDFormSet(instance=current_wb)
		
	return render_to_response('form.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))

def waybill_validate_form_update(request,wb_id):
	current_wb =  Waybill.objects.get(id=wb_id)
	lti_code = current_wb.ltiNumber
	current_lti = ltioriginal.objects.filter(CODE = lti_code)
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	class LoadingDetailDispatchForm(ModelForm):
		siNo= ModelChoiceField(queryset=ltioriginal.objects.all())
		numberUnitsLoaded=forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		numberUnitsGood= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		numberUnitsLost= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		numberUnitsDamaged= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		
		class Meta:
			model = LoadingDetail
			fields = ('wbNumber','siNo','numberUnitsLoaded','numberUnitsGood','numberUnitsLost','numberUnitsDamaged','unitsLostReason','unitsDamagedReason','unitsDamagedType','unitsLostType','overloadedUnits')

	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailDispatchForm,fk_name="wbNumber",  extra=0)

	if request.method == 'POST':
		form = WaybillFullForm(request.POST,instance=current_wb)
		formset = LDFormSet(request.POST,instance=current_wb)
		if form.is_valid() and formset.is_valid():
			wb_new = form.save()
			instances =formset.save()
			return HttpResponseRedirect('../viewwb/'+ str(wb_new.id)) #
	else:			
		form = WaybillFullForm(instance=current_wb)
		formset = LDFormSet(instance=current_wb)
		
	return render_to_response('waybill/waybill_detail.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))


 
def waybill_view(request,wb_id):
	waybill_instance = Waybill.objects.get(id=wb_id)
	lti_detail_items = ltioriginal.objects.filter(CODE=waybill_instance.ltiNumber)
	disp_person_object = EpicPerson.objects.get(person_pk=waybill_instance.dispatcherName)
	
	return render_to_response('waybill/waybill_detail_view.html',
							  {'object':waybill_instance,
							  'ltioriginal':lti_detail_items,
							  'disp_person':disp_person_object},
							  context_instance=RequestContext(request))



def waybill_view_reception(request,wb_id):
	waybill_instance = Waybill.objects.get(id=wb_id)
	lti_detail_items = ltioriginal.objects.filter(CODE=waybill_instance.ltiNumber)
	disp_person_object = EpicPerson.objects.get(person_pk=waybill_instance.dispatcherName)
	rec_person_object = EpicPerson.objects.get(person_pk=waybill_instance.recipientName)
	
	return render_to_response('waybill/waybill_detail_view_reception.html',
							  {'object':waybill_instance,
							  'ltioriginal':lti_detail_items,
							  'disp_person':disp_person_object,
							  'rec_person':rec_person_object},
							  context_instance=RequestContext(request))

def waybill_reception(request,wb_code):
	# get the LTI info
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	current_wb = Waybill.objects.get(id=wb_code)
	current_lti = current_wb.ltiNumber
	class LoadingDetailRecForm(ModelForm):
		siNo= ModelChoiceField(queryset=ltioriginal.objects.filter(CODE = current_lti),label='Commodity',)
		#siNo= forms.CharField(widget=forms.HiddenInput())
		numberUnitsLoaded= forms.CharField(widget=forms.HiddenInput())
		numberUnitsGood= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		numberUnitsLost= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		numberUnitsDamaged= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		
		class Meta:
			model = LoadingDetail
			fields = ('wbNumber','siNo','numberUnitsLoaded','numberUnitsGood','numberUnitsLost','numberUnitsDamaged','unitsLostReason','unitsDamagedReason','unitsDamagedType','unitsLostType','overloadedUnits')

	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailRecForm,fk_name="wbNumber",  extra=0)
	if request.method == 'POST':
		form = WaybillRecieptForm(request.POST,instance=current_wb)
		formset = LDFormSet(request.POST,instance=current_wb)
		if form.is_valid() and formset.is_valid():
			form.recipientTitle =  profile.compasUser.title
			form.recipientName=   profile.compasUser.person_pk
			wb_new = form.save()
			wb_new.recipientTitle =  profile.compasUser.title
			wb_new.recipientName=  profile.compasUser.person_pk
			wb_new.save()
			instances =formset.save()
			return HttpResponseRedirect('../viewwb_reception/'+ str(current_wb.id)) #
		
	else:
		if current_wb.recipientArrivalDate:
			form = WaybillRecieptForm(instance=current_wb)
			form.recipientTitle =  profile.compasUser.title
			form.recipientName=  profile.compasUser.last_name + ', ' +profile.compasUser.first_name
		else:
			form = WaybillRecieptForm(instance=current_wb,
			initial={
				'recipientArrivalDate':datetime.date.today(),
				'recipientStartDischargeDate':datetime.date.today(),
				'recipientEndDischargeDate':datetime.date.today(),
				'recipientName': 	 profile.compasUser.last_name + ', ' +profile.compasUser.first_name, 	
				'recipientTitle': 	 profile.compasUser.title,
			}
		)
		formset = LDFormSet(instance=current_wb)
	return render_to_response('recieveWaybill.html', 
			{'form': form,'lti_list':current_lti,'formset':formset,'profile':profile},
			context_instance=RequestContext(request))
#	return render_to_response('recieveWaybill.html',						  {'status':'to be implemented'},							  context_instance=RequestContext(request))



def waybill_reception_list(request):
	waybills = Waybill.objects.filter(recipientSigned = False)
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	return render_to_response('waybill/reception_list.html',
							  {'object_list':waybills,'profile':profile},
							  context_instance=RequestContext(request))

def waybill_search(request):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	search_string =  request.GET['wbnumber']
	found_wb=''
	
	found_wb = Waybill.objects.filter(waybillNumber__icontains=search_string)
	my_valid_wb=[]
	if profile != '' :	
		for waybill in found_wb:
			if profile.isCompasUser:
				my_valid_wb.append(waybill.id)
			elif profile.warehouses and waybill.loadingdetail_set.select_related()[0].siNo.ORIGIN_WH_CODE  == profile.warehouses.ORIGIN_WH_CODE:
				my_valid_wb.append(waybill.id)
			elif profile.receptionPoints and  waybill.loadingdetail_set.select_related()[0].siNo.CONSEGNEE_CODE == profile.receptionPoints.CONSEGNEE_CODE and waybill.loadingdetail_set.select_related()[0].siNo.DESTINATION_LOC_NAME == profile.receptionPoints.LOC_NAME :
				my_valid_wb.append(waybill.id)

	return render_to_response('list_waybills.html',
							  {'waybill_list':found_wb,'profile':profile, 'my_wb':my_valid_wb},
							  context_instance=RequestContext(request))

def waybillSearchResult(request):
	return render_to_response('status.html',
							  {'status':'selectAction not yet implemented'},
							  context_instance=RequestContext(request))


def waybillCreate(request,lti_code):
	# get the LTI info
	current_lti = ltioriginal.objects.filter(CODE = lti_code)
	
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	class LoadingDetailDispatchForm(ModelForm):
		siNo= ModelChoiceField(queryset=ltioriginal.objects.filter(CODE = lti_code),label='Commodity')
		#siNo= ModelChoiceField(queryset=ltioriginal.objects.raw("Select * from ltioriginal where CODE = '%s ",[lti_code]),label='Commodity')
		overload =  forms.BooleanField(required=False)
		class Meta:
			model = LoadingDetail
			fields = ('siNo','numberUnitsLoaded','wbNumber','overload')
		
#		def clean(self):
#			cleaned_data = self.cleaned_data
#			siNo = cleaned_data.get("siNo")
#			units = cleaned_data.get("numberUnitsLoaded")
#			overloaded = cleaned_data.get('overload')
#			theSI = ltioriginal.objects.get(id=siNo)
#			max_items = theSI.restant()
#			if units > max_items and not overloaded:
#				pass
#				
#			return cleaned_data
				
			


	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailDispatchForm,fk_name="wbNumber",  extra=5,max_num=5)

	if request.method == 'POST':
		form = WaybillForm(request.POST)
		formset = LDFormSet(request.POST)
		if form.is_valid() and formset.is_valid():
			wb_new = form.save()
			instances =formset.save(commit=False)
			wb_new.waybillNumber = 'ETS' + str(wb_new.id)
			for subform in instances:
				subform.wbNumber = wb_new
				subform.save()
			wb_new.save()
			return HttpResponseRedirect('../viewwb/'+ str(wb_new.id)) #
	else:
		
		form = WaybillForm(
			initial={
					'dispatcherName': 	 profile.compasUser.person_pk, 	
					'dispatcherTitle': 	 profile.compasUser.title,
					'ltiNumber':		 current_lti[0].CODE,
					'dateOfLoading':	 datetime.date.today(),
					'dateOfDispatch':	datetime.date.today(),
					'recipientLocation': current_lti[0].DESTINATION_LOC_NAME,
					'recipientConsingee':current_lti[0].CONSEGNEE_NAME,
					'transportContractor': current_lti[0].TRANSPORT_NAME,
					'waybillNumber':'N/A'
				}
		)
		formset = LDFormSet()
	return render_to_response('form.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))


def waybill_validateSelect(request):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	return render_to_response('selectValidateAction.html',
							  {'profile':profile},
							  context_instance=RequestContext(request))


def waybill_validate_form(request):

	ValidateFormset = modelformset_factory(Waybill, fields=('id','waybillValidated',),extra=0)
	
	
	if request.method == 'POST':
		formset = ValidateFormset(request.POST)
		if  formset.is_valid():
			formset.save()
		
	else:
		formset = ValidateFormset(queryset=Waybill.objects.filter(waybillValidated= False).filter(dispatcherSigned=True))
		
	
	return render_to_response('validateForm.html', {'formset':formset}, context_instance=RequestContext(request))
	




def waybill_validate_receipt_form(request):
	ValidateFormset = modelformset_factory(Waybill, fields=('id','waybillReceiptValidated',),extra=0)
	if request.method == 'POST':
		formset = ValidateFormset(request.POST)
		if  formset.is_valid():
			formset.save()
	else:
		formset = ValidateFormset(queryset=Waybill.objects.filter( waybillReceiptValidated = False).filter(recipientSigned=True).filter(waybillValidated= True))
	return render_to_response('validateReceiptForm.html', {'formset':formset}, context_instance=RequestContext(request))

def testform(request,lti_code):
	# get the LTI info
	current_lti = ltioriginal.objects.filter(CODE = lti_code)
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
	
	return render_to_response('blank.html',{'status':data},
							  context_instance=RequestContext(request))


def deserialize(request):
	waybillnumber=''
	for obj in serializers.deserialize("json", request.POST['wbdata']):
		if type(obj.object) is Waybill:
			waybillnumber= obj.object.id
	print waybillnumber
	return HttpResponseRedirect('../receive/'+ str(waybillnumber)) 
	
	
def custom_show_toolbar(request):
	return True

def printlistitem(list,index):
	print list(1)




#def get_or_create_profile(user):
 #   try:
 #	   profile = user.get_profile()
 #	   except ObjectDoesNotExist:
 #	   #create profile - CUSTOMIZE THIS LINE TO OYUR MODEL:
 #	   profile = UserProfile(karma='1', url='http://example.org', user=user)
 #	   profile.save()
 #   return profile