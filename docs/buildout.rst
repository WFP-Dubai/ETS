.. _buildout:

Buildout
======================================

Buildout is a Python-based build system for creating, assembling and deploying applications from multiple parts, some of which may be non-Python-based. It lets you create a buildout configuration and reproduce the same software later.
(http://www.buildout.org/)

We have four configurations for different purposes:

  - :ref:`base.cfg <base-configuration>`
  - :ref:`buildout.cfg <default-configuration>`
  - :ref:`production.cfg <production-configuration>`


.. _base-configuration:

Base configuration
------------------

This is a base configuration, which contains all dependencies from different repositories, script generators.

Contents:

  - :ref:`Git <base-git>`
  - :ref:`Subversion <base-svn>`
  - :ref:`base-interpreter`
  - :ref:`Sphinx configuration <base-sphinx>`
  - :ref:`base-cmds`


Code from repository is not stable, so we use it on our own risk.

.. _base-git:

Eggs from git repository
~~~~~~~~~~~~~~~~~~~~~~~~
  - django-app-media
  - django-mailer

Example of such parts::

  [django-mailer]
  recipe = zerokspot.recipe.git
  repository = http://github.com/spookylukey/django-mailer.git
  as_egg = true

Where recipe determines buildout recipe, which fetches code from repository, then builds package, installs dependencies.

.. _base-svn:

Packages from Subversion
~~~~~~~~~~~~~~~~~~~~~~~~
  - tabs

Code example:

.. literalinclude:: ../base.cfg
   :start-after: #svn part
   :end-before: #svn part ends


.. _base-interpreter:

Python interpreter
~~~~~~~~~~~~~~~~~~

This part is used for collecting all dependencies and creating proper PYTHONPATH.

.. literalinclude:: ../base.cfg
   :start-after: #interpreter part
   :end-before: #interpreter part end

.. _django-recipe

Django recipes
~~~~~~~~~~~~~~

We use special buildout recipe to fetch django and create `manage` and `wsgi` scripts.

There are two parts with different `settings`.

.. literalinclude:: ../base.cfg
   :start-after: #instance part
   :end-before: #instance part ends

This part downloads django 1.2.1, uses dependencies from :ref:`base-interpreter`, creates script `instance`, which acts like usual `manage`.
If we'd change wsgi equal to `True`, it'd create script `instance.wsgi`.

.. _base-sphinx:

Sphinx
~~~~~~

.. literalinclude:: ../base.cfg
   :start-after: #sphinx part
   :end-before: #sphinx part ends

Use script `make-docs` to create or update documentation.
Built docs will be stored in `build` folder.  

.. _base-cmds:

Shell commands
~~~~~~~~~~~~~~

.. literalinclude:: ../base.cfg
   :start-after: base-cmds=
   :end-before: cmds=


.. _default-configuration:

Development configuration
-------------------------

When user does not provide configuration file this will be used by default.

To inherit :ref:`base-configuration`:

.. literalinclude:: ../buildout.cfg
   :lines: 1-2

If you use `Eclipse IDE <http://www.eclipse.org>`_, this configuration will be useful for you. It contains special recipe:

.. literalinclude:: ../buildout.cfg
   :lines: 7-

This part registers all eggs and extra paths in eclipse project.


.. _production-configuration:

Production configuration
------------------------

This configurations sets up production environment.

Couple of thing we do:

  - append egg psycopg2
  - do check new versions of eggs
  - do not unzip eggs
  - install cmemcached
  - create wsgi script
