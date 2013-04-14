.. buildout:

Package structure
=================

Notes about packaging this system.


.. _package-structure:

Map
---------

Structure::

  ======================= =============================================================
  |-setup.py              :ref:`package-setup`
  |-base.cfg              :ref:`Base buildout configuration <base-configuration>`
  |-buildout.cfg          :ref:`Developement buildout configuration <default-configuration>`
  |-production.cfg        :ref:`Production buildout configuration <production-configuration>`
  |-docs                  Documentation
  |-src                   
    |---ets               :ref:`Configuration and common application <ets>`
    	|---models.py     :ref:`Models <ets_models>`
    	|---views.py      :ref:`Views <ets_views>`
    	|---utils.py      :ref:`Utils <ets_utils>`
    |---compas            :ref:`COMPAS mapping models <compas>`
  ======================= =============================================================


.. _package-setup:

Package setup
-------------

.. literalinclude:: ../setup.py
   :lines: 8,9,14-
