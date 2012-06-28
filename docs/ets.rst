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

.. _ets_commands:

Commands
========

.. _syncdb:

Special Syncdb
--------------

.. automodule:: ets.management.commands.syncdb
   :members:

.. _sync_compas:

Import data from COMPAS
-----------------------

.. automodule:: ets.management.commands.sync_compas
   :members:

.. _submit_waybills:

Submit created waybills back to COMPAS
--------------------------------------

.. automodule:: ets.management.commands.submit_waybills
   :members:

.. _export_compas:

Export data from COMPAS
-----------------------

.. automodule:: ets.management.commands.export_compas
   :members:

.. _import_file:

Import file with serialized and compressed data
-----------------------------------------------

.. automodule:: ets.management.commands.import_file
   :members:

.. _import_compas_full:

Import base data from compas
----------------------------

.. automodule:: ets.management.commands.import_compas_full
   :members:

.. _order_percentage:

Percentage of order executing
----------------------------

.. automodule:: ets.management.commands.order_percentage
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

.. _ets_reports:

Reports
=======

Piston is used for handling reports. We have a bunch of different handlers. And special emitter to create CSV.

.. automodule:: ets.api.handlers
   :members:

Every handler has at least one mapping line in urls.py.
