.. _tests:

Tests
*****

`Continuous integration test results <https://travis-ci.org/richardcornish/django-itunespodcast>`_ are available online.

However, you can also test the source code.

.. code-block:: bash

   $ workon myvenv
   $ django-admin test podcast.tests --settings="podcast.tests.settings"
   
   Creating test database for alias 'default'...
   ..........
   ----------------------------------------------------------------------
   Ran 1 test in 0.119s
   
   OK
   Destroying test database for alias 'default'...

A bundled settings file allows you to test the code without even creating a Django project.
