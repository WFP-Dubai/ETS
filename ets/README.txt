Frameworks Used:
Django
django-audit-log https://github.com/Atomidata/django-audit-log
MySQLdb
cx_Oracle

Requirements:
Oracle connection (using instantclient)
MySQL for server



README.txt					This file
TODO.txt					
__init__.py*				Standard Django
apache/						Config for apache using mod_wsgi
config/						Config for Development
manage.py*					Standard Django
media/
settings.py*				Modified to run config/$comutername$ settings
settings_default.py*
settings_production.py		Settigns for oPt Jerusalem Production (pointed to from apache/django.wsgi)
settings_training.py		Settigns for oPt Jerusalem Training (pointed to from apache/training_django.wsgi)
updatecompas.py*
urls.py*
waybill/				



VM Configuration:

To use the VM You need to do some configurations and need some information

IP to Comaps station(s):
Username/Password for the Compas Station (Might be standard...)
Dedicated IP for the VM: <iphost>
Hostname for the VM Host: <namehost>

How to configure the application IP/hostname?
If you prefer to configure the network manually you can run the following commands in the Virtual Machine:
Stop the network:
  $ sudo ifdown eth0

Your local network uses one of the following IP addresses:
  192.168.X.X
  172.X.X.X
  10.X.X.X
Depending on your network configuration you should use a different netmask. If you know a free IP address in your local network that the Virtual Machine could use, you can configure the network manually, for example:
 $ sudo ifconfig eth0 <iphost> netmask 255.255.255.0 up 

You can access the web application from any computer of your network at 192.168.1.234.



add fields:
!!!!
