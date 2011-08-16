.. installation_procedure:

**********************
Installation procedure
**********************

Here is a quick and dirty guide, that will help you to install system in different cases.


.. _dependencies:

Dependencies
============
  
Following names of package are called so in debian package system::
  
  sudo apt-get install python git-core python-dev python-setuptools gettext  
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

Oracle client
-------------

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
