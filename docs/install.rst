.. installation_procedure:

**********************
Installation procedure
**********************

Here is a quick and dirty guide, that will help you to install system in different cases.


.. _dependencies:

Dependencies
============
  
Following names of package are called so in debian package system::
  
  sudo apt-get install python git-core python-dev python-setuptools gettext libpq-dev
  sudo easy_install -U zc.buildout

.. _development-environment:  

Development environment
=======================

Change directory to project's root.

Build project
-------------

Build project using buildout and run it::

  python ./bootstrap.py; ./bin/buildout; ./bin/instance runserver
  
If you user Pydev, change last command as follows::

  ./bin/instance runserver -c ./pydev.cfg

Test environment
----------------

Go to http://localhost:8000/admin/

- Default Admin account

  username/e-mail: admin
  
  password: admin


.. _production-server:

Production server
=================

Production dependencies
------------
  
Following names of package are called so in debian package system::
  
  sudo apt-get install libpq-dev libaio-dev

Nginx
-------------

/etc/nginx/sites-available/ETS::

  server {
    listen <REAL_IP>:80;
    server_name ubuntu;

    access_log /var/log/ETS/nginx_access.log;
    error_log /var/log/ETS/nginx_error.log;

    location / {
      proxy_pass    http://127.0.0.1:80/;
      include       /etc/nginx/proxy.conf;
    }

    location /static/ {
      root /opt/ETS/;
      expires 5d;
    }

    location /media/ {
      root /opt/ETS/;
      expires 5d;
    }
  }


/etc/nginx/proxy.conf::
  
  proxy_redirect              off;
  proxy_set_header            Host $host;
  proxy_set_header            X-Real-IP $remote_addr;
  proxy_set_header            X-Forwarded-For $proxy_add_x_forwarded_for;
  client_max_body_size        10m;
  client_body_buffer_size     128k;
  proxy_connect_timeout       90;
  proxy_send_timeout          90;
  proxy_read_timeout          90;
  proxy_buffer_size           4k;
  proxy_buffers               4 32k;
  proxy_busy_buffers_size     64k;
  proxy_temp_file_write_size  64k;


Apache
-------------

/etc/apache2/ports.conf::
  
  NameVirtualHost 127.0.0.1:80
  Listen 127.0.0.1:80

  <IfModule mod_ssl.c>
    Listen 443
  </IfModule>

  <IfModule mod_gnutls.c>
    Listen 443
  </IfModule>


/etc/apache2/sites-available/main::
  
  <VirtualHost 127.0.0.1:80>
    ServerAdmin admin@ubuntu

    <Directory /opt/ETS/parts>
      Order deny,allow
      Allow from all
    </Directory>
    <Directory /opt/ETS/src>
      Order deny,allow
      Allow from all
    </Directory>

    WSGIScriptAlias / /opt/ETS/bin/instance.wsgi
    WSGIDaemonProcess main user=www-data group=www-data threads=25
    WSGIProcessGroup main
  
    LogLevel debug
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>

Download project from GitHub
----------------------------

  cd /opt/
  sudo git clone https://predatell@github.com/WFP-Dubai/ETS.git

Setting of Database
----------------------------

/opt/ETS/src/ets/settings/local.py::
    
  DEFAULT_DATABASE = {
	'NAME': 'ets',
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'HOST': '127.0.0.1',
	'USER': 'ets',
	'PASSWORD': 'ets',
  }

  sudo su - postgres
  createuser -dSRP ets
  createdb ets -O ets

Oracle client
-------------

Ubuntu 64
~~~~~~~~~

Installation of packeges::

  cd /opt/ETS/oracle/
  sudo dpkg -i *.deb
  sudo -i pip install cx-Oracle

Set environment variables::
 
  sudo touch /etc/ld.so.conf.d/ora-inst-cl-11.2.0.2.conf
  sudo echo "/usr/lib/oracle/11.2/client/lib" > /etc/ld.so.conf.d/ora-inst-cl-11.2.0.2.conf
  
  
Add to /etc/bash.bashrc::

  # oracle env
  export ORACLE_BASE=/usr/lib/oracle
  export ORACLE_HOME=$ORACLE_BASE/11.2/client64
  export LD_LIBRARY_PATH=$ORACLE_HOME/lib
  export PATH=$ORACLE_HOME/bin:$PATH
  export PATH=$ORACLE_HOME/lib:$PATH
  

Mac OS X
~~~~~~~~

1. Download following packages::

  http://download.oracle.com/otn/mac/instantclient/10204/instantclient-basic-10.2.0.4.0-macosx-x64.zip
  http://download.oracle.com/otn/mac/instantclient/10204/instantclient-jdbc-10.2.0.4.0-macosx-x64.zip
  http://download.oracle.com/otn/mac/instantclient/10204/instantclient-sqlplus-10.2.0.4.0-macosx-x64.zip
  http://download.oracle.com/otn/mac/instantclient/10204/instantclient-sdk-10.2.0.4.0-macosx-x64.zip
    
2. Unzip the packages into a single directory such as "instantclient".
3. Set the library loading path in your environment to the directory in Step 2 ("instantclient").
4. Create symlink for the library::
  
  cd <instantclient>
  ln -s libclntsh.dylib.10.1 libclntsh.dylib
   
4. Set environment variables::
  
  echo "export PATH=<instantclient directory>:$PATH" >> ~/.profile
  echo "export DYLD_LIBRARY_PATH=<instantclient directory>:$DYLD_LIBRARY_PATH" >> ~/.profile
   
5. Restart terminal and start your application.


Build project
-------------

Build project using buildout and run it::

  sudo python bootstrap.py
  sudo ./bin/buildout -c production.cfg
  sudo chown -R www-dada:www-data /opt/ETS
  sudo ./bin/instance createsuperuser