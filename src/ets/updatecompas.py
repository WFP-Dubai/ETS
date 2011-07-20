#!/usr/bin/env python
import urllib2
proxy_handler = urllib2.ProxyHandler( {} )
opener = urllib2.build_opener( proxy_handler, urllib2.HTTPBasicAuthHandler() )
urllib2.install_opener( opener )
myurl = urllib2.urlopen( 'http://localhost/ets/waybill/import' )
#print myurl.readlines()
