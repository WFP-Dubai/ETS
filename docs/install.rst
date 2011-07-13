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


.. _development-environment:  

Development environment
=======================

Change directory to project's root.

Specific settings
-----------------

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
