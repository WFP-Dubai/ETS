'''
Created on 03/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, ModelChoiceField, ModelForm
from django.forms.fields import BooleanField, CharField, TextInput
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from offliner.models import Waybill, LtiOriginal, LoadingDetail, EpicPerson, Places, WaybillSynchroState 
from offliner.forms import WaybillForm, LoadingDetailDispatchForm, WaybillRecieptForm, ImportFileForm
from offliner.tools import wb_compress, wb_compress_repr ,restant_si, new_waybill_no, \
                           synchronize_waybill, synchronize_stocks, synchronize_ltis, \
                           synchronize_receipt_waybills, wb_uncompress_repr


   
def select_action(request):
    '''
    View: select_action 
    URL: /offliner/select-action
    Template: /ets/offliner/templates/select_action.html
    Show choises of possible actions.
    '''       
    return render_to_response('select_action.html', context_instance=RequestContext(request, {'import_form':ImportFileForm()}))


def ltis_list(request):
    '''
    View: ltis_list 
    URL: ets/offliner/list/
    Template: /ets/offliner/templates/lti/ltis_list.html
    Show the LTIs that are in the specific warehouse.
    '''       
    # Verify if filtering by manager is required
    ltis = LtiOriginal.owned.values('code', 'destination_loc_name', 'consegnee_name', 'lti_date').distinct()
    
    # Finished LTIs
    still_ltis = []
    for lti in ltis:
        listOfSI_withDeduction = restant_si(lti['code'])
        for item in listOfSI_withDeduction:
            if item.CurrentAmount > 0 and not lti in still_ltis:
                still_ltis.append(lti)
    
    data_dict = {
                 'ltis':still_ltis, 
                 'WAREHOUSE_CODE':settings.OFFLINE_ORIGIN_WH_CODE
    }
    
    return render_to_response('lti/ltis_list.html', data_dict, context_instance=RequestContext(request))


def waybills_list(request):
    '''
    View: waybills_list 
    URL: ets/offliner/waybill/list/
    Template: /ets/offliner/templates/waybill/waybills_list.html
    Show the Waybills that are in the specific warehouse.
    ''' 
    # Verify if filtering by manager is required  
    waybills_list = Waybill.owned.order_by('-pk')
    
    data_dict = {
                 'waybill_list':waybills_list
    }
    
    return render_to_response('waybill/waybills_list.html', data_dict, context_instance=RequestContext(request))
    

def lti_detail(request, lti_code):    
    '''
    View: lti_detail 
    URL: ets/offliner/info/(lti_code)
    Template: /ets/offliner/templates/lti/lti_detail.html
    Show the detail of LtiOriginal and link to create related Waybill.
    '''
    detailed_lti = LtiOriginal.objects.filter(code=lti_code)
    listOfWaybills = Waybill.objects.filter(invalidated=False).filter(ltiNumber=lti_code)
    listOfSI_withDeduction = restant_si(lti_code)
    lti_more_wb = False
    
    for item in listOfSI_withDeduction:
        if item.CurrentAmount > 0:
            lti_more_wb = True
    
    data_dict = {
                 'detailed':detailed_lti, 
                 'lti_id':lti_code, 
                 'listOfWaybills':listOfWaybills, 
                 'listOfSI_withDeduction':listOfSI_withDeduction, 
                 'moreWBs':lti_more_wb
    }
            
    return render_to_response('lti/lti_detail.html', data_dict, context_instance=RequestContext(request))


def waybill_view(request, wb_id):   
    '''
    View: waybill_view 
    URL: ets/offliner/viewwb/(wb_id)
    Template: /ets/offliner/waybill/print/waybill_detail.html
    Show the detail of a Waybill.
    '''    
    try:               
        waybill_instance = Waybill.objects.get(id=wb_id)
        zippedWB = wb_compress_repr(wb_id)
        lti_detail_items = LtiOriginal.objects.filter(code=waybill_instance.ltiNumber)
        number_of_lines = waybill_instance.loadingdetail_set.select_related().count()
        extra_lines = 5 - number_of_lines
        my_empty = [''] * extra_lines
        try:
            disp_person_object = EpicPerson.objects.get(person_pk=waybill_instance.dispatcherName)
        except:
            disp_person_object = ''
        try:
            rec_person_object = EpicPerson.objects.get(person_pk=waybill_instance.recipientName)
        except:
            rec_person_object = ''
    except:
        return HttpResponseRedirect(reverse(select_action))
    
    data_dict = {
                 'object':waybill_instance,
                 'LtiOriginal':lti_detail_items,
                 'disp_person':disp_person_object,
                 'rec_person':rec_person_object,
                 'extra_lines':my_empty,
                 'zippedWB':zippedWB,
    }
    
#    print zippedWB

    return render_to_response('waybill/print/waybill_detail.html', data_dict, context_instance=RequestContext(request))


def waybill_create(request, lti_code):
    '''
    View: waybill_create 
    URL: ets/offliner/create/(lti_code)
    Template: /ets/offliner/templates/waybill/waybill_create.html
    Show the Waybill create form.
    '''
    # get the LTI info
    current_lti = LtiOriginal.objects.filter(code=lti_code)
    print current_lti[0].destination_loc_name

    class LoadingDetailDispatchForm(ModelForm):
        siNo = ModelChoiceField(queryset=LtiOriginal.objects.filter(code=lti_code), label='Commodity')
        overload = BooleanField(required=False)
        
        class Meta:
            model = LoadingDetail
            fields = ('siNo', 'numberUnitsLoaded', 'wbNumber', 'overloadedUnits', 'overOffloadUnits')
        
        def clean(self):
            #print "cleaning"
            cleaned = self.cleaned_data
            siNo = cleaned.get("siNo")
            units = cleaned.get("numberUnitsLoaded")
            overloaded = cleaned.get('overloadedUnits')
            max_items = siNo.restant2()

            if units > max_items + self.instance.numberUnitsLoaded and  overloaded == False: #and not overloaded:
                myerror = "Overloaded!"
                self._errors['numberUnitsLoaded'] = self._errors.get('numberUnitsLoaded', [])
                self._errors['numberUnitsLoaded'].append(myerror)
                raise ValidationError(myerror)
            return cleaned
       
    LDFormSet = inlineformset_factory(Waybill, LoadingDetail, LoadingDetailDispatchForm, fk_name="wbNumber", extra=5, max_num=5)
    print current_lti[0].destination_loc_name
    current_wh = ''
    if request.method == 'POST':
        form = WaybillForm(request.POST)
        print current_lti[0].destination_loc_name
        form.fields["destinationWarehouse"].queryset = Places.objects.filter(geo_name=current_lti[0].destination_loc_name)
        form.initial['dispatcherName'] = settings.USER_DISPATCHER_NAME  
        form.initial['dispatcherTitle'] = settings.USER_DISPATCHER_TITLE
        ## Make Better using the organization_id
        formset = LDFormSet(request.POST)
#        tempinstances = formset.save(commit=False)

        if form.is_valid() and formset.is_valid():
            wb_new = form.save()
            instances = formset.save(commit=False)
            wb_new.waybillNumber = new_waybill_no(wb_new)
            for subform in instances:
                subform.wbNumber = wb_new
                subform.save()
            wb_new.save()
            
#            Moved in observers.py
#            # initialize the waybill synchro state
#            waybillSynchroState = WaybillSynchroState()
#            waybillSynchroState.waybill = Waybill.objects.get(pk=wb_new.id)
#            waybillSynchroState.save()
            
#            Moved in observers.py
#            # try to call an exposed view of waybill (online) application for waybill upload
#            synchronize_waybill(wb_new.id)
            
            return HttpResponseRedirect('../viewwb/' + str(wb_new.id))
        else:
            pass
            #loggit(formset.errors)
            #loggit(form.errors)
    else:
        qs = Places.objects.filter(geo_name=current_lti[0].destination_loc_name).filter(organization_id=current_lti[0].consegnee_code)
        if len(qs) == 0:
            qs = Places.objects.filter(geo_name=current_lti[0].destination_loc_name)
        else:
            current_wh = qs[0]
        form = WaybillForm(
            initial={
                     'dispatcherName': settings.USER_DISPATCHER_NAME,
                     'dispatcherTitle': settings.USER_DISPATCHER_TITLE,
                     'ltiNumber': current_lti[0].code,
                     'dateOfLoading': datetime.date.today(),
                     'dateOfDispatch': datetime.date.today(),
                     'recipientLocation': current_lti[0].destination_loc_name,
                     'recipientConsingee': current_lti[0].consegnee_name,
                     'transportContractor': current_lti[0].transport_name,
                     'invalidated': 'False',
                     'destinationWarehouse': current_wh,
                     'waybillNumber': 'N/A'
            }
        )
        form.fields["destinationWarehouse"].queryset = qs
        #print current_lti[0].consegnee_code

        formset = LDFormSet()
        
    data_dict = {
                 'form': form, 
                 'lti_list':current_lti, 
                 'formset':formset
    } 
        
    return render_to_response('waybill/waybill_create.html', data_dict, context_instance=RequestContext(request))


def waybill_upload(request, wb_id):
    '''
    View: waybill_upload 
    URL: synchronize_waybill/(wb_id)
    Template: /ets/offliner/templates/waybill/waybills_list.html
    Uploades a Waybill from offline application to online application. 
    '''  

    warning_message = None

    try:
        wb_id = int(wb_id)

        # try to call an exposed url of online application for upload Waybill
        response_message = synchronize_waybill(wb_id)

        # If the service response is SYNCHRONIZATION_DONE then mark the waybill as synchronized.
        if response_message == 'SYNCHRONIZATION_DONE':
            waybillSynchroState = WaybillSynchroState.objects.get(waybill__id=wb_id)
            waybillSynchroState.synchronized = True
            waybillSynchroState.save()
        else:
            warning_message = 'Waybill upload can\'t be performed, verify your connection'

    except Exception:
        warning_message = 'Waybill upload can\'t be performed, verify data integrity'

    #print warning_message
    if warning_message:
        messages.add_message(request, messages.WARNING, warning_message)

    return HttpResponseRedirect(reverse(waybills_list))


def stock_download(request): 
    '''
    View: stock_download 
    URL: synchronize_stocks/
    Template: /ets/offliner/templates/select_action.html
    Downloades all EpicStocks related to the specific warehouse from online application to offline application. 
    '''  
    # try to call an exposed url of online application for download EpicStocks    
    message = synchronize_stocks(settings.OFFLINE_ORIGIN_WH_CODE)
    
    messages.add_message(request, messages.INFO, message)   

    return HttpResponseRedirect(reverse('offliner.views.select_action'))


def lti_download(request):
    '''
    View: lti_download 
    URL: synchronize_ltis/
    Template: /ets/offliner/templates/select_action.html
    Downloades all LtiOriginals related to the specific warehouse from online application to offline application. 
    '''  
    # try to call an exposed url of online application for download LtiOriginals      
    message = synchronize_ltis(settings.OFFLINE_ORIGIN_WH_CODE)
    
    messages.add_message(request, messages.INFO, message)

    return HttpResponseRedirect(reverse('offliner.views.select_action'))
    
    
def waybill_finalize_dispatch_offline(request,wb_id):
    '''
    View: waybill_finalize_dispatch
    URL: ets/waybill/dispatch
    Templet:None
    called when user pushes Print Original on dispatch
    Redirects to Lti Details
    '''
    current_wb =  Waybill.objects.get(id=wb_id)
    current_wb.transportDispachSigned=True
    current_wb.transportDispachSignedTimestamp=datetime.datetime.now()
    current_wb.dispatcherSigned=True
    current_wb.auditComment='Print Dispatch Original'
#     for lineitem in current_wb.loadingdetail_set.select_related():
#         lineitem.siNo.reducesi(lineitem.numberUnitsLoaded)
    current_wb.save()
    status = 'Waybill '+ current_wb.waybillNumber +' Dispatch Signed'
#    messages.add_message(request, messages.INFO, status)
    return HttpResponseRedirect(reverse(lti_detail,args=[current_wb.ltiNumber]))


def    waybill_finalize_receipt_offline(request,wb_id):
    '''
    View: waybill_finalize_receipt 
    URL:ets/waybill/receipt/
    Template:None
    Redirects to Lti Details
    Called when user pushes Print Original on Receipt
    '''
    try:
        current_wb = Waybill.objects.get(id=wb_id)
        current_wb.recipientSigned=True
        current_wb.transportDeliverySignedTimestamp=datetime.datetime.now()
        current_wb.recipientSignedTimestamp=datetime.datetime.now()    
        current_wb.transportDeliverySigned=True
        current_wb.auditComment='Print Dispatch Receipt'
        current_wb.save()
        status = 'Waybill '+ current_wb.waybillNumber +' Receipt Signed'
        messages.add_message(request, messages.INFO, status)
    except:
        pass
    return HttpResponseRedirect(reverse(waybill_reception_list)) 


def waybill_reception_list(request):
    '''
    View: waybill_reception_list 
    URL: ets/offliner/waybill/reception/list/
    Template: /ets/offliner/templates/waybill/waybill_reception_list.html
    Show the reception Waybills that are for the specific warehouse.
    '''   
       
    waybills_list = Waybill.objects.filter(destinationWarehouse__pk=settings.OFFLINE_ORIGIN_WH_CODE).filter(recipientSigned = False).order_by('-pk')
    
    data_dict = {
                 'waybill_list':waybills_list
    }
    
    return render_to_response('waybill/waybill_reception_list.html', data_dict, context_instance=RequestContext(request))


def receipt_waybill_download(request):
    '''
    View: receipt_waybill_download 
    URL: synchronize_receipt_waybills/
    Template: /ets/offliner/templates/select_action.html
    Downloades all receipt Waybill related to the specific warehouse from online application to offline application. 
    '''  
    # try to call an exposed url of online application for download receipt Waybills      
    message = synchronize_receipt_waybills(settings.OFFLINE_ORIGIN_WH_CODE)
    
    messages.add_message(request, messages.INFO, message)

    return HttpResponseRedirect(reverse('offliner.views.select_action'))


def waybill_reception(request,wb_code):
    '''
    View: waybill_reception 
    URL: offliner/waybill/receive/(wb_code)
    '''
    current_wb = Waybill.objects.get(id=wb_code)
    current_lti = current_wb.ltiNumber
        
    class LoadingDetailRecForm(ModelForm):
        siNo = ModelChoiceField(queryset=LtiOriginal.objects.filter(code = current_lti), label='Commodity',)
        numberUnitsGood = CharField(widget=TextInput(attrs={'size':'5'}), required=False)
        numberUnitsLost = CharField(widget=TextInput(attrs={'size':'5'}), required=False)
        numberUnitsDamaged = CharField(widget=TextInput(attrs={'size':'5'}), required=False)
        
        class Meta:
            model = LoadingDetail
            fields = ('wbNumber','siNo','numberUnitsGood','numberUnitsLost','numberUnitsDamaged','unitsLostReason',
                      'unitsDamagedReason','unitsDamagedType','unitsLostType','overloadedUnits','overOffloadUnits')
            
        def clean_unitsLostReason(self):
            my_losses = self.cleaned_data.get('numberUnitsLost')
            my_lr = self.cleaned_data.get('unitsLostReason')
            if float(my_losses) >0 :
                if my_lr == None:
                    raise ValidationError("You have forgotten to select the Loss Reason")    
            return my_lr

        def clean_unitsDamagedReason(self):
            my_damage = self.cleaned_data.get('numberUnitsDamaged')
            my_dr = self.cleaned_data.get('unitsDamagedReason')
            if float(my_damage)>0:
                if my_dr == None:
                    raise ValidationError("You have forgotten to select the Damage Reason")
            return my_dr

        def clean_unitsLostType(self):
            my_losses = self.cleaned_data.get('numberUnitsLost')
            my_lr = self.cleaned_data.get('unitsLostType')
            if float(my_losses) >0 :
                if my_lr == None:
                    raise ValidationError("You have forgotten to select the Loss Type")    
            return my_lr

        def clean_unitsDamagedType(self):
            my_damage = self.cleaned_data.get('numberUnitsDamaged')
            my_dr = self.cleaned_data.get('unitsDamagedType')
            if float(my_damage)>0:
                if my_dr == None:
                    raise ValidationError("You have forgotten to select the Damage Type")
            return my_dr
      
        def clean(self):
            cleaned = self.cleaned_data
            numberUnitsGood = float(cleaned.get('numberUnitsGood'))
            loadedUnits = float(self.instance.numberUnitsLoaded)
            damadgedUnits = float(cleaned.get('numberUnitsDamaged'))
            lostUnits =float(cleaned.get('numberUnitsLost'))
            totaloffload = float(numberUnitsGood+damadgedUnits+ lostUnits)
            if not cleaned.get('overOffloadUnits'):
                if not totaloffload == loadedUnits:
                    myerror = ''
                    if totaloffload > loadedUnits:
                        myerror =  "%.3f Units loaded but %.3f units accounted for"%(loadedUnits,totaloffload)
                    if totaloffload < loadedUnits:
                        myerror =  "%.3f Units loaded but only %.3f units accounted for"%(loadedUnits,totaloffload)
                    self._errors['numberUnitsGood'] = self._errors.get('numberUnitsGood', [])
                    self._errors['numberUnitsGood'].append(myerror)
                    raise ValidationError(myerror)
            return cleaned
        
    LDFormSet = inlineformset_factory(Waybill, LoadingDetail, LoadingDetailRecForm, fk_name="wbNumber", extra=0)
    
    if request.method == 'POST':

        form = WaybillRecieptForm(request.POST,instance=current_wb)

        formset = LDFormSet(request.POST,instance=current_wb)
        if form.is_valid() and formset.is_valid():
            form.recipientTitle = settings.USER_RECEIVER_TITLE  #request.user.profile.compasUser.title
            form.recipientName = settings.USER_RECEIVER_NAME   #request.user.profile.compasUser.person_pk
            wb_new = form.save()
            
            wb_new.recipientTitle = settings.USER_RECEIVER_TITLE   #request.user.profile.compasUser.title
            wb_new.recipientName = settings.USER_RECEIVER_NAME  #request.user.profile.compasUser.person_pk
            wb_new.auditComment = 'Receipt Action'
            wb_new.save()
            
            instances = formset.save()
            # @todo Change me!!!!
            return HttpResponseRedirect('../viewwb_reception/'+ str(current_wb.id)) #
        else:
            print formset.errors
            print form.errors
    else:
        if current_wb.recipientArrivalDate:
            form = WaybillRecieptForm(instance=current_wb)
            form.recipientTitle = settings.USER_RECEIVER_TITLE   #request.user.profile.compasUser.title
            form.recipientName = settings.USER_LAST_NAME + ', ' + settings.USER_FIRST_NAME #request.user.profile.compasUser.last_name + ', ' +  request.user.profile.compasUser.first_name
        else:
            form = WaybillRecieptForm(instance=current_wb,
            initial={
                     'recipientArrivalDate': datetime.date.today(),
                     'recipientStartDischargeDate': datetime.date.today(),
                     'recipientEndDischargeDate': datetime.date.today(),
                     'recipientName': settings.USER_LAST_NAME + ', ' + settings.USER_FIRST_NAME, #request.user.profile.compasUser.last_name + ', ' +  request.user.profile.compasUser.first_name,     
                     'recipientTitle': settings.USER_RECEIVER_TITLE,      #request.user.profile.compasUser.title,
            }
        )
        formset = LDFormSet(instance=current_wb)
        
    data_dict = {
                 'form': form,
                 'lti_list': current_lti,
                 'formset': formset
    }    
    
    return render_to_response('waybill/waybill_receive.html', data_dict, context_instance=RequestContext(request))


def waybill_view_reception(request,wb_id):
    '''
    View: waybill_view_reception 
    URL: offliner/waybill/viewwb_reception/(wb_id)
    Template: waybill/print/waybill_detail_view_reception.html
    Show the detail of a receipt Waybill.
    '''
    
    rec_person_object = ''
    disp_person_object =''
    zippedWB=''
    try:
        waybill_instance = Waybill.objects.get(id=wb_id)
        lti_detail_items = LtiOriginal.objects.filter(code=waybill_instance.ltiNumber)
        number_of_lines = waybill_instance.loadingdetail_set.select_related().count()
        extra_lines = 5 - number_of_lines
        my_empty = ['']*extra_lines
        zippedWB = wb_compress_repr(wb_id)    
    except:
        return HttpResponseRedirect(reverse(select_action))
    
    try:
        disp_person_object = EpicPerson.objects.get(person_pk=waybill_instance.dispatcherName)
        rec_person_object = EpicPerson.objects.get(person_pk=waybill_instance.recipientName)
    except:
        pass
    
    data_dict = {
                 'object':waybill_instance,
                 'LtiOriginal':lti_detail_items,
                 'disp_person':disp_person_object,
                 'rec_person':rec_person_object,
                 'extra_lines':my_empty,
                 'zippedWB':zippedWB
    }     
    
    return render_to_response('waybill/print/waybill_detail_reception.html', data_dict, context_instance=RequestContext(request))
    

def waybill_export(request):
    '''
    View: waybill_export 
    URL: waybill/export/
    Produces a file containing the json representation of the Waybill data identified by the wbnumber request param 
    and data of related LoadingDetails.
    The file named waybill-(wbnumber).json is returned in response. 
    ''' 
    
    response = HttpResponseRedirect(reverse('offliner.views.select_action'))
    
    if request.method == 'GET':
        try:
            search_string = request.GET['wbnumber']
        except:
            search_string = None
        
        waybill_founded = Waybill.objects.filter(invalidated=False).filter(waybillNumber=search_string).count()>0
        
        if not search_string or not waybill_founded:
            messages.add_message(request, messages.WARNING, 'Please specify a valid waybill number')            
      
        else:                                
            waybill_to_serialize = Waybill.objects.filter(invalidated=False).filter(waybillNumber=search_string)[0]
            
            from kiowa.db.utils import instance_as_dict     
            
            waybill_dict = instance_as_dict(waybill_to_serialize, exclude='id')
            
            loading_detail_list_dict = []
            for loading_detail in waybill_to_serialize.loadingdetail_set.select_related():
                loading_detail_list_dict.append(instance_as_dict(loading_detail, exclude=('id','wbNumber')))
            
            import simplejson as json 
            from kiowa.utils.encode import DecimalJSONEncoder       
            serialized_waybill = json.dumps([waybill_dict,loading_detail_list_dict], cls=DecimalJSONEncoder)
            
            response = HttpResponse(serialized_waybill, mimetype='application/json')
            response['Content-Disposition'] = 'filename=waybill-' + search_string + '.json'
        
    return response


def waybill_import(request):
    '''
    View: waybill_import 
    URL: waybill/import/
    Persists the data in the file containing the json representation of the Waybill and related LoadingDetails.
    ''' 
    
    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            try:           
                import simplejson as json
                
                file_content = file.read()
                
#                print 777777777777777777777, file_content
#                print 888888888888888888888, type(file_content)
                
                deserialized_content = json.loads(file_content)
                
                waybill = deserialized_content[0]
                           
                # Verify if the waybill is for this specific warehouse          
                if waybill.get('destinationWarehouse') <> settings.OFFLINE_ORIGIN_WH_CODE:
                    messages.add_message(request, messages.WARNING, 'This waybill is not for your warehouse')    
                
                # Save Waybill:   
                wb, unused = Waybill.objects.get_or_create(waybillNumber=waybill['waybillNumber'], destinationWarehouse=Places.objects.get(org_code=waybill['destinationWarehouse']))
                    
                for k,v in waybill.items():
                    if not k=='destinationWarehouse':
                        setattr(wb, k, v)                
                wb.save()
                
                # Save related LoadingDeatils: 
                wb.loadingdetail_set.all().delete()
                              
                loading_details = deserialized_content[1]
                for el in loading_details:
                    ld = LoadingDetail()
                    for k,v in el.items():
                        if not k=='siNo':
                            setattr(ld, k, v)
                    # setting foreign keys 
                    ld.siNo = LtiOriginal.objects.get(lti_pk=el['siNo'])
                    ld.wbNumber = wb
                    ld.save()
            except:
                messages.add_message(request, messages.ERROR, 'The contents of the selected file can not be loaded') 
            
        else:
            form = ImportFileForm()
                
    return HttpResponseRedirect(reverse('offliner.views.select_action'))


def booleanize(boolean_str):
    return boolean_str in [u'True', u'T', u'true', u'1', True, str(True)]


def waybill_scan(request):
    '''
    View: waybill_scan
    URL: waybill/scan/
    Persists the data in the text containing the compressed representation of the Waybill and related LoadingDetails.
    '''

    if request.method == 'POST':

        wb_compressed_str = request.POST['wb_compressed_str']

        try:
            wb_uncompressed = wb_uncompress_repr(wb_compressed_str)

            waybill_positional_dict = wb_uncompressed[0]

            from structures import waybill_positional2named_dict
            waybill_dict = waybill_positional2named_dict(waybill_positional_dict)

            # Verify if the waybill is for this specific warehouse
            if waybill_dict.get('destinationWarehouse') != settings.OFFLINE_ORIGIN_WH_CODE:
                messages.add_message(request, messages.WARNING, 'This waybill is not for your warehouse')

            # Save Waybill:
            waybill, unused = Waybill.objects.get_or_create(waybillNumber=waybill_dict['waybillNumber'], destinationWarehouse=Places.objects.get(org_code=waybill_dict['destinationWarehouse']))

            for k,v in waybill_dict.items():
                if not k=='destinationWarehouse':
                    setattr(waybill, k, booleanize(v) if type(waybill.__getattribute__(k))==bool else v)
                else:
                    setattr(waybill, 'destinationWarehouse', Places.objects.get(org_code=v))
            waybill.save()

            # Save related LoadingDeatils:
            waybill.loadingdetail_set.all().delete()

            loadingdetails_positional_dicts = wb_uncompressed[1]

            from structures import loadingdetail_positional2named_dict
            loadingdetails_dicts = []
            for x in loadingdetails_positional_dicts:
                loadingdetail_dict = loadingdetail_positional2named_dict(x)
                loadingdetails_dicts.append(loadingdetail_dict)

            for el in loadingdetails_dicts:
                ld = LoadingDetail()
                for k,v in el.items():
                    if not k=='siNo':
                        setattr(ld, k, booleanize(v) if type(ld.__getattribute__(k))==bool else v)
                # setting foreign keys
                ld.siNo = LtiOriginal.objects.get(lti_pk=el['siNo'])
                ld.wbNumber = waybill
                ld.save()

        except Exception, e:
            messages.add_message(request, messages.ERROR, 'The contents of the text can not be loaded')

    return HttpResponseRedirect(reverse('offliner.views.select_action'))
