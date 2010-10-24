# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login,logout
from django.core import serializers
from django.core.urlresolvers import reverse
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory,modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext,Library, Node
from ets.waybill.compas import *
from ets.waybill.forms import *
from ets.waybill.models import *
from ets.waybill.tools import *
import datetime
import os,StringIO, zlib,base64,string





def prep_req(request):
	return{'user': request.user}
	

def homepage(request):
	""" 
	View:
	homepage /
	redirects you to the selectAction page
	"""
	return HttpResponseRedirect(reverse(selectAction))
							  
@login_required	
def selectAction(request):
	"""
	View:
	selectAction /ets/select-action
	Gives the loggedin user a choise of possible actions sepending on roles
	template:
	/ets/waybill/templates/selectAction.html
	"""
	print request
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	return render_to_response('selectAction.html',
							  {'profile':profile},
							  context_instance=RequestContext(request))

@login_required	
def listOfLtis(request,origin):
	"""
	View:
	listOfLtis waybill/list/{{warehouse}}
	Shows the LTIs that are in a specific warehouse
	template:
	/ets/waybill/templates/ltis.html
	"""
	ltis = ltioriginal.objects.ltiCodesByWH(origin)
	#ltis_qs =ltioriginal.objects.values( 'CODE','DESTINATION_LOC_NAME','CONSEGNEE_NAME','LTI_DATE' ).distinct()
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	still_ltis=[]
	# finished ltis
	for lti in ltis:
		listOfSI_withDeduction = restant_si(lti[0])
		for item in listOfSI_withDeduction:
			if item.CurrentAmount > 0:
				if not lti in still_ltis:
					still_ltis.append(lti)
	return render_to_response('ltis.html',
							  {'ltis':still_ltis,'profile':profile},
							  context_instance=RequestContext(request))

## repurposed show all ltis 
def ltis(request):
	"""
	View:
	ltis waybill/list
	Shows the LTIs that are in a specific warehouse
	template:
	/ets/waybill/templates/ltis.html
	"""
	ltis = ltioriginal.objects.ltiCodesAll()
	#ltis_qs =ltioriginal.objects.values( 'CODE','DESTINATION_LOC_NAME','CONSEGNEE_NAME','LTI_DATE' ).distinct()
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	still_ltis=[]
	# finished ltis
	for lti in ltis:
		listOfSI_withDeduction = restant_si(lti[0])
		for item in listOfSI_withDeduction:
			if item.CurrentAmount > 0:
				if not lti in still_ltis:
					still_ltis.append(lti)
	return render_to_response('ltis_all.html',
							  {'ltis':still_ltis,'profile':profile},
							  context_instance=RequestContext(request))
## ^ NOT IN USE


def ltis_redirect_wh(request):
	"""
	View:
	ltis_redirect_wh waybill/list/
	automatically redirects user to his dispatch point wh to listOfLtis
	template:
	None
	"""
	wh_code = request.GET['dispatch_point']
	return HttpResponseRedirect(reverse(listOfLtis ,args=[wh_code]))

def import_ltis(request):
	"""
	View:
	import_ltis ets/waybill/import
	Executes Imports of LTIs Persons Stock and updates SiTracker
	template:
	/ets/waybill/templates/status.html
	"""
	#Copy Persons
	update_persons()
	#copy LTIs
	listRecepients = ReceptionPoint.objects.values('CONSEGNEE_CODE').distinct()
	listDispatchers = DispatchPoint.objects.values('ORIGIN_WH_CODE').distinct()
	
	## TODO: Fix so ltis imported are not expired
	original = ltioriginal.objects.using('compas').filter(REQUESTED_DISPATCH_DATE__gt='2010-06-28')
	
	for myrecord in original:
		for rec in listRecepients:
			if myrecord.CONSEGNEE_CODE in  rec['CONSEGNEE_CODE']:
				for disp in listDispatchers:
					if myrecord.ORIGIN_WH_CODE in disp['ORIGIN_WH_CODE']:
						myrecord.save(using='default')
						try:
							mysist =myrecord.sitracker #try to get it, if it exist check LTI NOU and update if not equal
							if mysist.number_units_start != myrecord.NUMBER_OF_UNITS:
								try:
									change = myrecord.NUMBER_OF_UNITS - mysist.number_units_start 
									mysist.number_units_left =	mysist.number_units_left + change	
									mysist.save(using='default')	
								except:
									pass
						except:
							mysist = SiTracker()
							mysist.LTI=myrecord
							mysist.number_units_left = myrecord.NUMBER_OF_UNITS
							mysist.number_units_start = myrecord.NUMBER_OF_UNITS
							mysist.save(using='default')
							
	#cleanup ltis loop and see if changes to lti ie deleted rows
	current = ltioriginal.objects.all()
	for c in current:
		if c not in original:
			#c.delete() # fix this as it removes even if in use!!!
			c.remove_lti()

	
	
	#UPDATE GEO
	import_geo()	
	#Copy Stock
	#EpicStock.objects.all().delete()
	import_stock()
	
	
	status = 'Import Finished'
	return render_to_response('status.html',
							  {'status':status},
							  context_instance=RequestContext(request))



def lti_detail_url(request,lti_code):	
	"""
	View:
	lti_detail_url waybill/info/(lti_code)
	Show detail of LTI and link to create waybill
	template:
	/ets/waybill/templates/detailed_lti.html
	"""
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	
	detailed_lti = ltioriginal.objects.filter(CODE=lti_code)
	listOfWaybills = Waybill.objects.filter(invalidated=False).filter(ltiNumber=lti_code)
	listOfSI_withDeduction = restant_si(lti_code)
	lti_more_wb=False
	for item in listOfSI_withDeduction:
		if item.CurrentAmount > 0:
			lti_more_wb=True
	return render_to_response('detailed_lti.html',
							  {'detailed':detailed_lti,'lti_id':lti_code,'profile':profile,'listOfWaybills':listOfWaybills,'listOfSI_withDeduction':listOfSI_withDeduction,'moreWBs':lti_more_wb},
							  context_instance=RequestContext(request))
							  
@login_required
def dispatch(request):
	"""
	View:
	dispatch waybill/dispatch
	template:
	Redirects to Lti Details.
	"""
	try:
		return HttpResponseRedirect(reverse(listOfLtis,args=[request.user.get_profile().warehouses.ORIGIN_WH_CODE])) 
	except:
		return HttpResponseRedirect(reverse(selectAction))

#### Waybill Views
@login_required
def waybill_create(request,lti_pk):
	try:
		detailed_lti = ltioriginal.objects.get(LTI_PK=lti_pk)
	except:
		detailed_lti = ''
	return render_to_response('detailed_waybill.html',
							  {'detailed':detailed_lti,'lti_id':lti_pk},
							  context_instance=RequestContext(request))

@login_required
def waybill_finalize_dispatch(request,wb_id):
	"""
	View:
	waybill_finalize_dispatch waybill/dispatch
	called when user pushes Print Original on dispatch
	Redirects to Lti Details
	"""
	current_wb =  Waybill.objects.get(id=wb_id)
	current_wb.transportDispachSigned=True
	current_wb.transportDispachSignedTimestamp=datetime.datetime.now()
	current_wb.dispatcherSigned=True
	for lineitem in current_wb.loadingdetail_set.select_related():
#		print lineitem.numberUnitsLoaded
#		print lineitem.siNo.restant()
		lineitem.siNo.reducesi(lineitem.numberUnitsLoaded)
	current_wb.save()
	return HttpResponseRedirect(reverse(lti_detail_url,args=[current_wb.ltiNumber]))
	
@login_required
def	waybill_finalize_reciept(request,wb_id):
	"""
	View:
	waybill_finalize_dispatch waybill/dispatch
	called when user pushes Print Original on dispatch
	Redirects to Lti Details
	"""
	try:
		current_wb = Waybill.objects.get(id=wb_id)
		current_wb.recipientSigned=True
		current_wb.transportDeliverySignedTimestamp=datetime.datetime.now()
		current_wb.recipientSignedTimestamp=datetime.datetime.now()	
		current_wb.transportDeliverySigned=True
		current_wb.save()
	except:
		 return HttpResponseRedirect(reverse(selectAction))
	return HttpResponseRedirect(reverse(waybill_view_reception, args=[current_wb.id])) 

@login_required
def dispatchToCompas(request):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	list_waybills = Waybill.objects.filter(invalidated=False).filter(waybillValidated = True).filter(	waybillSentToCompas = False)
	the_compas = compas_write()
	error_message = ''
	error_codes = ''
	for waybill in list_waybills:
		# call compas and read return
		status_wb = the_compas.write_dispatch_waybill_compas(waybill.id)
		if  status_wb:
			#aok
			waybill.waybillSentToCompas=True
			waybill.save()
		else:
			# error here
			error_message +=waybill.waybillNumber + '-' + the_compas.ErrorMessages
			error_codes +=waybill.waybillNumber +'-'+ the_compas.ErrorCodes
	return render_to_response('list_waybills_compas.html',
							  {'waybill_list':list_waybills,'profile':profile, 'error_message':error_message,'error_codes':error_codes},
							  context_instance=RequestContext(request))
							  
def singleWBDispatchToCompas(request,wb_id):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	waybill = Waybill.objects.get(id=wb_id)
#	print waybill.waybillNumber
	the_compas = compas_write()
	error_message = ''
	error_codes = ''
	status_wb = the_compas.write_dispatch_waybill_compas(wb_id)
	if  status_wb:
		#aok
		waybill.waybillSentToCompas=True
		waybill.save()
	else:
		# error here
		#print waybill.waybillNumber
		#log error.
		errorlog = ''
		errorlog = loggerCompas()
		errorlog.wb = waybill
		errorlog.user = request.user
		errorlog.errorDisp = the_compas.ErrorMessages
		errorlog.timestamp = datetime.datetime.now()
		errorlog.save()

		waybill.waybillValidated =False
		waybill.save()
		error_message +=waybill.waybillNumber + '-' + the_compas.ErrorMessages
		error_codes +=waybill.waybillNumber +'-'+ the_compas.ErrorCodes
# add field to say compas erroradd logging
	return render_to_response('status_waybill_compas.html',
							  {'waybill':waybill,'profile':profile, 'error_message':error_message,'error_codes':error_codes},
							  context_instance=RequestContext(request))
	

def singleWBReceiptToCompas(request,wb_id):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	waybill = Waybill.objects.get(id=wb_id)
	the_compas = compas_write()
	error_message = ''
	error_codes = ''
	status_wb = the_compas.write_receipt_waybill_compas(waybill.id)
	if  status_wb:
		#aok
		waybill.waybillSentToCompas=True
		waybill.save()
	else:
		# error here
		#log error.
		errorlog = ''
		errorlog = loggerCompas()
		errorlog.wb = waybill
		errorlog.user = request.user
		errorlog.errorRec = the_compas.ErrorMessages
		errorlog.timestamp = datetime.datetime.now()
		errorlog.save()
		waybill.waybillReceiptValidated =False
		waybill.save()
		error_message +=waybill.waybillNumber + '-' + the_compas.ErrorMessages
		error_codes +=waybill.waybillNumber +'-'+ the_compas.ErrorCodes
# add field to say compas error/add logging
	return render_to_response('status_waybill_compas_rec.html',
							  {'waybill':waybill,
							  'profile':profile,
							  'error_message':error_message,
							  'error_codes':error_codes},
							  context_instance=RequestContext(request))	
	
def listCompasWB(request):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	list_waybills_disp = Waybill.objects.filter(invalidated=False).filter(waybillSentToCompas = True)
	list_waybills_rec = Waybill.objects.filter(invalidated=False).filter(waybillRecSentToCompas = True)
	return render_to_response('list_waybills_compas_all.html',
							  {'waybill_list':list_waybills_disp,'waybill_list_rec':list_waybills_rec,'profile':profile},
							  context_instance=RequestContext(request))

@login_required
def receiptToCompas(request):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		print 'no person'
	list_waybills = Waybill.objects.filter(invalidated=False).filter(waybillReceiptValidated = True).filter(waybillRecSentToCompas = False).filter(waybillSentToCompas=True)
	the_compas = compas_write()
	error_message = ''
	error_codes = ''
	for waybill in list_waybills:
		# call compas and read return
		status_wb = the_compas.write_receipt_waybill_compas(waybill.id)
		if  status_wb:
			#print "ok"
			waybill.waybillRecSentToCompas=True
			waybill.save()
		else:
			#print 'error'
			error_message +=waybill.waybillNumber + '-' + the_compas.ErrorMessages
			error_codes +=waybill.waybillNumber +'-'+ the_compas.ErrorCodes
	return render_to_response('list_waybills_compas_received.html',
							  {'waybill_list':list_waybills,'profile':profile, 'error_message':error_message,'error_codes':error_codes},
							  context_instance=RequestContext(request))

def invalidate_waybill(request,wb_id):
	#first mark waybill invalidate, then zero the stock usage for each line and update the si table
	current_wb = Waybill.objects.get(id=wb_id)
	for lineitem in current_wb.loadingdetail_set.select_related():
		lineitem.siNo.restoresi(lineitem.numberUnitsLoaded)
		lineitem.numberUnitsLoaded = 0
		lineitem.save()
	current_wb.invalidated=True
	current_wb.save()
	status = 'Waybill %s has now been Removed'%(current_wb.waybillNumber)
	return render_to_response('status.html',
							  {'status':status},
							  context_instance=RequestContext(request))

@login_required
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
			return HttpResponseRedirect(reverse(reset_waybill))
	else:			
		form = WaybillFullForm(instance=current_wb)
		formset = LDFormSet(instance=current_wb)
	return render_to_response('waybill/waybill_detail.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))


@login_required
def waybill_view(request,wb_id):
	try:
		waybill_instance = Waybill.objects.get(id=wb_id)
		zippedWB = wb_compress(wb_id)
		lti_detail_items = ltioriginal.objects.filter(CODE=waybill_instance.ltiNumber)
		number_of_lines = waybill_instance.loadingdetail_set.select_related().count()
		extra_lines = 5 - number_of_lines
		my_empty = ['']*extra_lines
		try:
			disp_person_object = EpicPerson.objects.get(person_pk=waybill_instance.dispatcherName)
		except:
			disp_person_object=''
		try:
			rec_person_object = EpicPerson.objects.get(person_pk=waybill_instance.recipientName)
		except:
			rec_person_object=''
	except:
		return HttpResponseRedirect(reverse(selectAction))
	return render_to_response('waybill/print/waybill_detail_view.html',
							  {'object':waybill_instance,
							  'ltioriginal':lti_detail_items,
							  'disp_person':disp_person_object,
							  'rec_person':rec_person_object,
							  'extra_lines':my_empty,
							  'zippedWB':zippedWB,
							  },
							  context_instance=RequestContext(request))

@login_required
def waybill_view_reception(request,wb_id):
	rec_person_object = ''
	disp_person_object =''
	zippedWB=''
	try:
		waybill_instance = Waybill.objects.get(id=wb_id)
		lti_detail_items = ltioriginal.objects.filter(CODE=waybill_instance.ltiNumber)
		number_of_lines = waybill_instance.loadingdetail_set.select_related().count()
		extra_lines = 5 - number_of_lines
		my_empty = ['']*extra_lines
		zippedWB = wb_compress(wb_id)	
	except:
		return HttpResponseRedirect(reverse(selectAction))
	try:
		disp_person_object = EpicPerson.objects.get(person_pk=waybill_instance.dispatcherName)
		rec_person_object = EpicPerson.objects.get(person_pk=waybill_instance.recipientName)
	except:
		pass
	return render_to_response('waybill/print/waybill_detail_view_reception.html',
							  {'object':waybill_instance,
							  'ltioriginal':lti_detail_items,
							  'disp_person':disp_person_object,
							  'rec_person':rec_person_object,
							  'extra_lines':my_empty,
							  'zippedWB':zippedWB},
							  context_instance=RequestContext(request))

#@login_required
# def reset_waybill(request):
# 	profile = ''
# 	try:
# 		profile=request.user.get_profile()
# 	except:
# 		pass
# 		
# 	if profile.superUser:
# 		waybills = Waybill.objects.filter(invalidated=False).filter(waybillSentToCompas = False)
# 		
# 		return render_to_response('edit_wb_list.html',
# 							  {'profile':profile,'waybill_list':waybills},
# 							  context_instance=RequestContext(request))
# 	elif profile.readerUser:
# 		waybills = Waybill.objects.filter(invalidated=False).filter(waybillSentToCompas = False)
# 		return render_to_response('edit_wb_list.html',
# 							  {'profile':profile,'waybill_list':waybills},
# 							  context_instance=RequestContext(request))
# 
# 	else:
# 		return render_to_response('selectAction.html',
# 							  {'profile':profile},
# 							  context_instance=RequestContext(request))
# 	


@login_required
def waybill_reception(request,wb_code):
	# get the LTI info
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	current_wb = Waybill.objects.get(id=wb_code)
	current_lti = current_wb.ltiNumber
	if  profile.isReciever or profile.superUser:
		pass
	else:
		return HttpResponseRedirect(reverse(waybill_view ,args=[wb_code]))
	class LoadingDetailRecForm(ModelForm):
		siNo= ModelChoiceField(queryset=ltioriginal.objects.filter(CODE = current_lti),label='Commodity',)
		numberUnitsGood= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		numberUnitsLost= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		numberUnitsDamaged= forms.CharField(widget=forms.TextInput(attrs={'size':'5'}),required=False)
		class Meta:
			model = LoadingDetail
			fields = ('wbNumber','siNo','numberUnitsGood','numberUnitsLost','numberUnitsDamaged','unitsLostReason','unitsDamagedReason','unitsDamagedType','unitsLostType','overloadedUnits')
		def clean_unitsLostReason(self):
			#cleaned_data = self.cleaned_data
			my_losses = self.cleaned_data.get('numberUnitsLost')
			my_lr = self.cleaned_data.get('unitsLostReason')
			if  float(my_losses) >0 :
				if my_lr == None:
					raise forms.ValidationError("You have forgotten to select the Loss Reason")	
			return my_lr


		def clean_unitsDamagedReason(self):
			my_damage = self.cleaned_data.get('numberUnitsDamaged')
			my_dr = self.cleaned_data.get('unitsDamagedReason')

			if float(my_damage)>0:
				if my_dr == None:
					raise forms.ValidationError("You have forgotten to select the Damage Reason")
			return my_dr

		def clean_unitsLostType(self):
			#cleaned_data = self.cleaned_data
			my_losses = self.cleaned_data.get('numberUnitsLost')
			my_lr = self.cleaned_data.get('unitsLostType')
			if  float(my_losses) >0 :
				if my_lr == None:
					raise forms.ValidationError("You have forgotten to select the Loss Type")	
			return my_lr


		def clean_unitsDamagedType(self):
			my_damage = self.cleaned_data.get('numberUnitsDamaged')
			my_dr = self.cleaned_data.get('unitsDamagedType')

			if float(my_damage)>0:
				if my_dr == None:
					raise forms.ValidationError("You have forgotten to select the Damage Type")
			return my_dr
		
		def clean(self):
			cleaned = self.cleaned_data
			numberUnitsGood = float(cleaned.get('numberUnitsGood'))
			loadedUnits = float(self.instance.numberUnitsLoaded)
			damadgedUnits = float(cleaned.get('numberUnitsDamaged'))
			lostUnits =float(cleaned.get('numberUnitsLost'))
			totaloffload = numberUnitsGood+damadgedUnits+ lostUnits
			if not totaloffload == loadedUnits:
				myerror = ''
				if totaloffload > loadedUnits:
					myerror =  "%.2f Units loaded but %.2f units accounted for"%(loadedUnits,totaloffload)
				if totaloffload < loadedUnits:
					myerror =  "%.2f Units loaded but only %.2f units accounted for"%(loadedUnits,totaloffload)
				
				self._errors['numberUnitsGood'] = self._errors.get('numberUnitsGood', [])
				self._errors['numberUnitsGood'].append(myerror)
				raise forms.ValidationError(myerror)
			
			
			return cleaned
			

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
			print formset.errors
			print form.errors
		
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
	return render_to_response('receiveWaybill.html', 
			{'form': form,'lti_list':current_lti,'formset':formset,'profile':profile},
			context_instance=RequestContext(request))



@login_required
def waybill_reception_list(request):
	waybills = Waybill.objects.filter(invalidated=False).filter(recipientSigned = False)
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
	
	search_string=''
	found_wb=''
	try:
		search_string =  request.GET['wbnumber']
	except:
		pass
	

	
	found_wb = Waybill.objects.filter(invalidated=False).filter(waybillNumber__icontains=search_string)
	my_valid_wb=[]
	curr_wh_disp = ''
	
	if profile != '' :	
		for waybill in found_wb:
			try:
				curr_wh_disp = waybill.loadingdetail_set.select_related()[0].siNo.ORIGIN_WH_CODE
			except:
				curr_wh_disp = ''
			try:
				curr_wh_rec = waybill.loadingdetail_set.select_related()[0].siNo.CONSEGNEE_CODE
				curr_loc = waybill.loadingdetail_set.select_related()[0].siNo.DESTINATION_LOC_NAME
			except:
				curr_wh_rec = ''
				curr_loc = ''				

			if profile.isCompasUser or profile.readerUser:
				my_valid_wb.append(waybill.id)
			elif profile.warehouses and curr_wh_disp  == profile.warehouses.ORIGIN_WH_CODE:
				my_valid_wb.append(waybill.id)
			elif profile.receptionPoints and  curr_wh_rec == profile.receptionPoints.CONSEGNEE_CODE and curr_loc == profile.receptionPoints.LOC_NAME :
				my_valid_wb.append(waybill.id)
	
	return render_to_response('list_waybills.html',
							  {'waybill_list':found_wb,'profile':profile, 'my_wb':my_valid_wb},
							  context_instance=RequestContext(request))



### Create Waybill 
@login_required
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
		overload =  forms.BooleanField(required=False)
		class Meta:
			model = LoadingDetail
			fields = ('siNo','numberUnitsLoaded','wbNumber','overloadedUnits')
		
		def clean(self):
  			#print "cleaning"
  			cleaned = self.cleaned_data
  			siNo = cleaned.get("siNo")
  			units = cleaned.get("numberUnitsLoaded")
  			overloaded = cleaned.get('overloadedUnits')
  			max_items = siNo.restant2()
  			#print max_items
  			#print long(units)
  			#print units > max_items+self.instance.numberUnitsLoaded
  			if units > max_items+self.instance.numberUnitsLoaded and  overloaded == False: #and not overloaded:
  				myerror = "Overloaded!"
  				self._errors['numberUnitsLoaded'] = self._errors.get('numberUnitsLoaded', [])
 				self._errors['numberUnitsLoaded'].append(myerror)
 				raise forms.ValidationError(myerror)
   			return cleaned
   			
	
	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailDispatchForm,fk_name="wbNumber",  extra=5,max_num=5)

	if request.method == 'POST':
		form = WaybillForm(request.POST)
		form.fields["destinationWarehouse"].queryset = places.objects.filter(GEO_NAME = current_lti[0].DESTINATION_LOC_NAME)
		formset = LDFormSet(request.POST)
#		tempinstances = formset.save(commit=False)
		if form.is_valid() and formset.is_valid():
			wb_new = form.save()
			instances = formset.save(commit=False)
			wb_new.waybillNumber = 'E' + '%04d' % wb_new.id
			for subform in instances:
				subform.wbNumber = wb_new
				subform.save()
			wb_new.save()
			return HttpResponseRedirect('../viewwb/'+ str(wb_new.id))
		else:
			print formset.errors
			print form.errors
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
					'invalidated':'False',
					'waybillNumber':'N/A'
				}
		)
		form.fields["destinationWarehouse"].queryset = places.objects.filter(GEO_NAME = current_lti[0].DESTINATION_LOC_NAME)
		formset = LDFormSet()
	return render_to_response('form.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))

@login_required
def waybill_edit(request,wb_id):
	try:
		current_wb =  Waybill.objects.get(id=wb_id)
		lti_code = current_wb.ltiNumber
		current_lti = ltioriginal.objects.filter(CODE = lti_code)
	except:
		currnet_wb =''
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	class LoadingDetailDispatchForm(ModelForm):
		siNo= ModelChoiceField(queryset=ltioriginal.objects.filter(CODE = lti_code),label='Commodity')
		class Meta:
			model = LoadingDetail
			fields = ('id','siNo','numberUnitsLoaded','wbNumber','overloadedUnits')
		def clean(self):
  			cleaned = self.cleaned_data
  			siNo = cleaned.get("siNo")
  			units = cleaned.get("numberUnitsLoaded")
  			overloaded = cleaned.get('overloadedUnits')
  			max_items = siNo.restant2()
  			if units > max_items+self.instance.numberUnitsLoaded and overloaded == False:
	  				myerror = "Overloaded!"
	  				self._errors['numberUnitsLoaded'] = self._errors.get('numberUnitsLoaded', [])
	 				self._errors['numberUnitsLoaded'].append(myerror)
 					raise forms.ValidationError(myerror)
   			return cleaned
	LDFormSet = inlineformset_factory(Waybill, LoadingDetail,LoadingDetailDispatchForm,fk_name="wbNumber",  extra=5,max_num=5)
	if request.method == 'POST':
		form = WaybillForm(request.POST,instance=current_wb)
		formset = LDFormSet(request.POST,instance=current_wb)
		if form.is_valid() and formset.is_valid():
			wb_new = form.save()
			instances =formset.save()
			return HttpResponseRedirect(reverse(waybill_view,args=[wb_new.id])) 
	else:			
		form = WaybillForm(instance=current_wb)
		form.fields["destinationWarehouse"].queryset = places.objects.filter(GEO_NAME = current_lti[0].DESTINATION_LOC_NAME)
		formset = LDFormSet(instance=current_wb)
	return render_to_response('form.html', {'form': form,'lti_list':current_lti,'formset':formset}, context_instance=RequestContext(request))

@login_required
def waybill_validateSelect(request):
	profile = ''
	try:
		profile=request.user.get_profile()
	except:
		pass
	return render_to_response('selectValidateAction.html',
							  {'profile':profile},
							  context_instance=RequestContext(request))

@login_required
def waybill_validate_dispatch_form(request):
	ValidateFormset = modelformset_factory(Waybill, fields=('id','waybillValidated',),extra=0)
	validatedWB = Waybill.objects.filter(invalidated=False).filter(waybillValidated= True).filter(waybillSentToCompas=False)
	if request.method == 'POST':
		formset = ValidateFormset(request.POST)
		if  formset.is_valid():
			formset.save()
		formset = ValidateFormset(queryset=Waybill.objects.filter(invalidated=False).filter(waybillValidated= False).filter(dispatcherSigned=True))
	else:
		formset = ValidateFormset(queryset=Waybill.objects.filter(invalidated=False).filter(waybillValidated= False).filter(dispatcherSigned=True))
	return render_to_response('validateForm.html', {'formset':formset,'validatedWB':validatedWB}, context_instance=RequestContext(request))
	
@login_required
def waybill_validate_receipt_form(request):
	ValidateFormset = modelformset_factory(Waybill, fields=('id','waybillReceiptValidated',),extra=0)
	validatedWB = Waybill.objects.filter(invalidated=False).filter(waybillReceiptValidated= True).filter(waybillRecSentToCompas=False)
	if request.method == 'POST':
		formset = ValidateFormset(request.POST)
		if  formset.is_valid():
			formset.save()
		formset = ValidateFormset(queryset=Waybill.objects.filter(invalidated=False).filter( waybillReceiptValidated = False).filter(recipientSigned=True).filter(waybillValidated= True))
	else:
		formset = ValidateFormset(queryset=Waybill.objects.filter(invalidated=False).filter( waybillReceiptValidated = False).filter(recipientSigned=True).filter(waybillValidated= True))
	return render_to_response('validateReceiptForm.html', {'formset':formset,'validatedWB':validatedWB}, context_instance=RequestContext(request))

@login_required
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

# Shows a page with the Serialized Waybill in comressed & uncompressed format
@login_required
def serialize(request,wb_code):
	waybill_to_serialize = Waybill.objects.filter(id=wb_code)
	items_to_serialize =''# waybill_to_serialize[0].loadingdetail_set.select_related()
	data = serializers.serialize('json',list(waybill_to_serialize)+list(items_to_serialize))	
	zippedWB = wb_compress(wb_code)
	return render_to_response('blank.html',{'status':data,'ziped':zippedWB},
							  context_instance=RequestContext(request))

## recives a POST with the comressed or uncompressed WB and sends you to the Reveive WB 
@login_required
def deserialize(request):
	waybillnumber=''
	wb_data = request.POST['wbdata']
	wb_serialized = ''
	if wb_data[0] == '[':
		wb_serialized = wb_data
	else:
		wb_serialized = un64unZip(wb_data)
	for obj in serializers.deserialize("json", wb_serialized):
		if type(obj.object) is Waybill:
			waybillnumber= obj.object.id
	return HttpResponseRedirect('../receive/'+ str(waybillnumber)) 

## Serialization of fixtures	
def fixtures_serialize():
	# serialise each of the fixtures 
	# 	DispatchPoint
	dispatchPointsData = DispatchPoint.objects.all()
	receptionPointData = ReceptionPoint.objects.all()
	packagingDescriptonShort = PackagingDescriptonShort.objects.all()
	lossesDamagesReason = LossesDamagesReason.objects.all()
	lossesDamagesType = LossesDamagesType.objects.all()	
	serialized_data = serializers.serialize('json',list(dispatchPointsData)+list(receptionPointData)+list(packagingDescriptonShort)+list(lossesDamagesReason)+list(lossesDamagesType))
	init_file = open('waybill/fixtures/initial_data.json','w')
	init_file.writelines(serialized_data)
	init_file.close()
	
def custom_show_toolbar(request):
	return True
	
def update_persons():
	"""
	Executes Imports of LTIs Persons
	"""
	originalPerson = EpicPerson.objects.using('compas').filter(org_unit_code='JERX001')
	for my_person in originalPerson:
		my_person.save(using='default')	
	
def import_geo():
	"""
	Executes Imports of places
	"""
	#UPDATE GEO
	try:
		my_geo = places.objects.using('compas').filter(COUNTRY_CODE='275')
		for the_geo in my_geo:
				the_geo.save(using='default')
	except:
		pass	
	try:
		my_geo = places.objects.using('compas').filter(COUNTRY_CODE='376')
		for the_geo in my_geo:
				the_geo.save(using='default')
	except:
		pass
	return True

def import_stock():
	"""
	Executes Imports of Stock
	"""
	originalStock = EpicStock.objects.using('compas')
	for myrecord in originalStock:
		myrecord.save(using='default')
	
	current_stock = EpicStock.objects.all()
	for item in current_stock:
		if item not in current_stock:
			item.number_of_units = 0;
			item.save()