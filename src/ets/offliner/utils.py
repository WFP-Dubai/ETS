import urllib2

def send_waybill(waybill):

    if waybill.transport_dispach_signed_date:
        data = waybill.serialize()
        return urllib2.urlopen(urllib2.Request('api_offline', data, {
                'Content-Type': 'application/json; charset=utf-8',
        }))
