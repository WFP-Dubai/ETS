.. buildout:

Package structure
=================

Notes about packaging this system.


.. _package-structure:

Map
---------

audio_books::
  ======================= =============================================================
  |-setup.py              :ref:`package-setup`
  |-base.cfg              :ref:`Base buildout configuration <base-configuration>`
  |-buildout.cfg          :ref:`Developement buildout configuration <default-configuration>`
  |-production.cfg        :ref:`Production buildout configuration <production-configuration>`
  |-cron                  :ref:`cron-scripts`
    |---daily.sh          :ref:`daily-tasks`
    |---often.sh          :ref:`often-tasks`
  |-docs                  Documentation
  |-src                   
    |---audio_books       Configuration and common application
  ======================= =============================================================


.. _package-setup:

Package setup
-------------

.. literalinclude:: ../setup.py
   :lines: 6,7,10,17-