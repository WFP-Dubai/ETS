.. _ets:

*****************************
ETS 
*****************************

Central application in the system.

.. _ets_models:

Models
======

.. automodule:: ets.models
   :members:

Inheritance diagrams
--------------------

.. inheritance-diagram:: ets.models

.. _ets_views:

Views
=====

.. automodule:: ets.views
   :members:


Forms
=====

.. automodule:: ets.forms
   :members:

Commands
========

.. _syncdb:

Special Syncdb
----------------

.. automodule:: ets.management.commands.syncdb
   :members:

.. _sync_compas:

Import data from COMPAS
-------------------------

.. automodule:: ets.management.commands.sync_compas
   :members:

.. _submit_waybills:

Submit created waybills back to COMPAS
--------------------------------------

.. automodule:: ets.management.commands.submit_waybills
   :members:

Middleware
==========

.. automodule:: ets.middleware
   :members:

.. _ets_utils:

Utils
=====

.. automodule:: ets.utils
   :members:
   
Settings
========

- **URL_PREFIX** -- site prefix,

Reports
=======

Piston is used for handling reports. We have a bunch of different handlers. And special emitter to create CSV.

.. automodule:: ets.api.handlers
   :members:

Every handler has at least one mapping line in urls.py.
