from django.db import models
from django.contrib import admin

# Create your models here.
class Commodity(models.Model):
	commodiryRef=models.TextField()
	commodityName=models.TextField()
	commodityType=models.TextField()
	
class LTI(models.Model):
	LTI_ID=models.CharField(max_length=25)
	CODE=models.CharField(max_length=25)
	LTI_DATE=models.DateTimeField()
	CONTRACT_CODE=models.CharField(max_length=20)
	EXPIRY_DATE=models.DateTimeField()
	ORIGIN_TYPE=models.CharField(max_length=1)	
	ORIGIN_LOCATION_CODE=models.CharField(max_length=10)
	INTVYG_CODE=models.CharField(max_length=25)
	INTDLV_CODE=models.DecimalField( max_digits=2, decimal_places=0)
	ORIGIN_CODE=models.CharField(max_length=13)
	ORIGIN_DESCR=models.CharField(max_length=50)
	DESTINATION_LOCATION_CODE=models.CharField(max_length=10)
	ORGANIZATION_ID	=models.CharField(max_length=12)
	REQUESTED_DISPATCH_DATE=models.DateTimeField()
	INSPECTION_INDICATOR=models.CharField(max_length=1)
	OFFICER_CODE=models.CharField(max_length=7)
	PERSON2_OUC=models.CharField(max_length=13)
	TITLE_OF_OFFICER=models.CharField(max_length=50)
	ISSUING_CODE=models.CharField(max_length=7)
	PERSON1_OUC=models.CharField(max_length=13)
	TITLE_OF_ISSUING=models.CharField(max_length=50)
	TRANSPORTER_CODE=models.CharField(max_length=4)
	SUPPLIER_OUC=models.CharField(max_length=13)
	TRANSPORT_RATE_TYPE=models.CharField(max_length=10)
	TRANSPORT_CURRENCY=models.CharField(max_length=3)
	TRANSPORT_RATE=models.DecimalField(max_digits=15, decimal_places=3)
	FUEL_ENTITLEMENT=models.DecimalField( max_digits=15, decimal_places=3)
	FUEL_RATE=models.DecimalField( max_digits=15, decimal_places=3)
	FUEL_CURRENCY=models.CharField(max_length=3)
	FOOD_RELEASE=models.CharField(max_length=6)
	REMARKS	=models.CharField(max_length=250)
	REMARKS_B=models.CharField(max_length=250)
	OBSERVATIONS=models.CharField(max_length=250)
	STATUS_INDICATOR=models.CharField(max_length=1)
	ORG_UNIT_CODE=models.CharField(max_length=13)
	PRINTED_INDICATOR=models.CharField(max_length=1)
	OFFID=models.CharField(max_length=13)
	SEND_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	RECV_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	LAST_MOD_USER=models.CharField(max_length=30)
	LAST_MOD_DATE=models.DateTimeField()

class LTIDetail(models.Model):
	LTI_ID=models.ForeignKey(LTI)
	SI_RECORD_ID=models.CharField(max_length=25)
	COMM_CATEGORY_CODE=models.CharField(max_length=9)
	COMMODITY_CODE=models.CharField(max_length=18)
	QUANTITY_NET=models.DecimalField( max_digits=11, decimal_places=3)
	QUANTITY_GROSS=models.DecimalField( max_digits=11, decimal_places=3)
	NUMBER_OF_UNITS=models.DecimalField( max_digits=7, decimal_places=0)
	UNIT_WEIGHT_NET=models.DecimalField( max_digits=8, decimal_places=3)
	UNIT_WEIGHT_GROSS=models.DecimalField( max_digits=8, decimal_places=3)
	OFFID=models.CharField(max_length=13)
	SEND_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	RECV_PACK=models.DecimalField( max_digits=20, decimal_places=0)
	LAST_MOD_USER=models.CharField(max_length=20)
	LAST_MOD_DATE=models.DateTimeField()


class WayBill(models.Model):
	ltiNumber=models.ForeignKey(LTI)
	waybillNumber=models.TextField()
	
	
class LoadingDetail(models.Model):
	wbNumber=models.ForeignKey(WayBill)
	siNo=models.IntegerField()
	commodity=models.ForeignKey(Commodity)
	
	
	
admin.site.register(Commodity)
admin.site.register(LTI)
admin.site.register(WayBill)
admin.site.register(LoadingDetail)
admin.site.register(LTIDetail)

