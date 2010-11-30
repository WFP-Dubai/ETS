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

def loggit(items):
# 	try:
# 		logfile = 'logg.txt'
# 		FILE = open(logfile,"a")
# 		FILE.write(str(datetime.datetime.now())+ ':'+items + '\n')
# 		FILE.close()
		print items
# 	except:
		pass	
	
def viewLog():
	try:
		logfile = 'logg.txt'
		FILE = open(logfile,"r")
		log = FILE.read()
		FILE.close()
		return log
	except:
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

def serialize_wb(wb_code):
	waybill_to_serialize = Waybill.objects.filter(id=wb_code)
	items_to_serialize = waybill_to_serialize[0].loadingdetail_set.select_related()
	lti_to_serialize =  ltioriginal.objects.filter(LTI_PK=items_to_serialize[0].siNo.LTI_PK)
	data = serializers.serialize('json',list(waybill_to_serialize)+list(items_to_serialize)+list(lti_to_serialize))
	return data

def wb_compress(wb_code):
	data = serialize_wb(wb_code)#serializers.serialize('json',list(waybill_to_serialize)+list(items_to_serialize)+list(lti_to_serialize))
	printIt( data)
	zippedData =	zipBase64(data)
	return zippedData


def zipBase64(data):
	zippedData = zlib.compress(data)
	base64Data = base64.b64encode(zippedData)
	return base64Data
	
def restant_si(lti_code):
	detailed_lti = ltioriginal.objects.filter(CODE=lti_code)
	listOfWaybills = Waybill.objects.filter(invalidated=False).filter(ltiNumber=lti_code).filter(waybillSentToCompas=False)
	listOfSI = []
#	listExl =removedLtis.objects.list()

	
	for lti in detailed_lti:
			if not removedLtis.objects.filter(lti = lti.LTI_PK):
				if lti.isBulk():
					listOfSI += [SIWithRestant(lti.SI_CODE,lti.QUANTITY_NET,lti.CMMNAME)]
					print 'bulk'
				else:
					listOfSI += [SIWithRestant(lti.SI_CODE,lti.NUMBER_OF_UNITS,lti.CMMNAME)]
					print 'not bulk'

 	for wb in listOfWaybills:
 		for loading in wb.loadingdetail_set.select_related():
 			for si in listOfSI:
 				if si.SINumber == loading.siNo.SI_CODE:
 					si.reduceCurrent(loading.numberUnitsLoaded)
 	return listOfSI
 	
##### Make Waybill number !!!! (make better)
def newWaybillNo(waybill):
    return 'E' + '%04d' % waybill.id

####
	
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
		if item not in originalStock:
			item.number_of_units = 0;
			item.save()
			
def import_lti():
	listRecepients = ReceptionPoint.objects.values('CONSEGNEE_CODE','LOCATION_CODE','ACTIVE_START_DATE').distinct()
	listDispatchers = DispatchPoint.objects.values('ORIGIN_WH_CODE','ACTIVE_START_DATE').distinct()
	# check what type is the comodity... if bulk swap
	
	## TODO: Fix so ltis imported are not expired
	original = ltioriginal.objects.using('compas').filter(REQUESTED_DISPATCH_DATE__gt='2010-06-28')
	# log each item
	for myrecord in original:
		not_in = True
		for rec in listRecepients:
			#print rec
			if myrecord.CONSEGNEE_CODE in rec['CONSEGNEE_CODE'] and myrecord.DESTINATION_LOCATION_CODE in rec['LOCATION_CODE'] and myrecord.LTI_DATE >  rec['ACTIVE_START_DATE']:
				for disp in listDispatchers:
					if myrecord.ORIGIN_WH_CODE in disp['ORIGIN_WH_CODE'] and myrecord.LTI_DATE >  disp['ACTIVE_START_DATE']:
						myrecord.save(using='default') ## here we import the record...
						try:
							myr = removedLtis.objects.get(lti=myrecord)
							myr.delete()
						except:
							pass
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
						not_in = False
						break
				not_in = False
				break
			else:
#				pass# not here (remove if it should no be here)
				try:
					ltioriginal.objects.get(id = myrecord.id)
				except:
					pass
				

		if not_in:
			pass#loggit('Not In %s'%myrecord)
		else:
			pass#loggit('In %s'%myrecord)
			#print rec

	#cleanup ltis loop and see if changes to lti ie deleted rows
	current = ltioriginal.objects.all()
	for c in current:
		if c not in original:
			c.remove_lti()
	#	if c.EXPIRY_DATE < datetime.date.today():
	#		c.remove_lti()

			
def printIt(line):
#	print line
	pass
	