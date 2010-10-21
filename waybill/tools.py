from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login,logout
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db import connections
from django.db import models
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory,modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext,Library, Node
from ets.waybill.compas import *
from ets.waybill.forms import *
from ets.waybill.models import *
from ets.waybill.tools import *
from ets.waybill.views import *
import cx_Oracle
import datetime
import os,StringIO, zlib,base64,string


def theHello():
	print 'hello'
	return 'hello'
	
def logger(action,user,datain,dataout):
	pass
	
def uniq(inlist):
    # order preserving
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques
    
#prints a list item....
def printlistitem(list,index):
	print list(index)

def printlist(list):
	for item in list:
		print item

# takes compressed base64 Data and uncompresses it
def un64unZip(data):
	data= string.replace(data,' ','+')
	zippedData = base64.b64decode(data)
	uncompressed = zlib.decompress(zippedData)	
	return uncompressed

# takes a wb id and returns a zipped base64 string of the serialized object // ?use table to reduce column names save 1000 bytes?
def wb_compress(wb_code):
	waybill_to_serialize = Waybill.objects.filter(id=wb_code)
	items_to_serialize = waybill_to_serialize[0].loadingdetail_set.select_related()
	lti_to_serialize =  ltioriginal.objects.filter(LTI_PK=items_to_serialize[0].siNo.LTI_PK)
	#print lti_to_serialize
	data = serializers.serialize('json',list(waybill_to_serialize)+list(items_to_serialize)+list(lti_to_serialize))
	zippedData =	zipBase64(data)
	return zippedData


def zipBase64(data):
	zippedData = zlib.compress(data)
	base64Data = base64.b64encode(zippedData)
	return base64Data
	
def restant_si(lti_code):
	detailed_lti = ltioriginal.objects.filter(CODE=lti_code)
	listOfWaybills = Waybill.objects.filter(invalidated=False).filter(ltiNumber=lti_code)
	listOfSI = []
#	listExl =removedLtis.objects.list()

	for lti in detailed_lti:
			if not removedLtis.objects.filter(lti = lti.LTI_PK):
				listOfSI += [SIWithRestant(lti.SI_CODE,lti.NUMBER_OF_UNITS,lti.CMMNAME)]

 	for wb in listOfWaybills:
 		for loading in wb.loadingdetail_set.select_related():
 			for si in listOfSI:
 				if si.SINumber == loading.siNo.SI_CODE:
 					si.reduceCurrent(loading.numberUnitsLoaded)
 	return listOfSI