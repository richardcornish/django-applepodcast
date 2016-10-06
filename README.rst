.. image:: https://django-itunespodcast.readthedocs.io/en/latest/_images/logo.svg?

Django iTunes Podcast
*********************

|PyPI version|_ |Build status|_

.. |PyPI version| image::
   https://badge.fury.io/py/django-itunespodcast.svg
.. _PyPI version: https://pypi.python.org/pypi/django-itunespodcast

.. |Build status| image::
   https://travis-ci.org/richardcornish/django-itunespodcast.svg?branch=master
.. _Build status: https://travis-ci.org/richardcornish/django-itunespodcast

**Django iTunes Podcast** is a `Django podcast application <https://docs.djangoproject.com/en/1.10/intro/reusable-apps/>`_ optimized for the `iTunes Store <https://podcastsconnect.apple.com/>`_.

* `Package distribution <https://pypi.python.org/pypi/django-itunespodcast>`_
* `Code repository <https://github.com/richardcornish/django-itunespodcast>`_
* `Documentation <https://django-itunespodcast.readthedocs.io/>`_
* `Tests <https://travis-ci.org/richardcornish/django-itunespodcast>`_

An online demo also exists.

* `Online demo <https://djangoitunespodcastdemo.herokuapp.com/podcasts/>`_
* `Code repository <https://github.com/richardcornish/djangoitunespodcastdemo>`_

Install
=======

.. code-block:: bash

   $ pip install django-itunespodcast

Add to ``settings.py``.

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       'podcast',
   ]

Add to ``urls.py``.

.. code-block:: python

   from django.conf.urls import url, include

   urlpatterns = [
       # ...
       url(r'^podcast/', include('podcast.urls')),
   ]

Migrate the database.

.. code-block:: bash

   $ python manage.py migrate

Load the fixtures.

.. code-block:: bash

   $ python manage.py loaddata podcast_category.json

Usage
=====

Run the local server.

.. code-block:: bash

   $ python manage.py runserver

Visit either the show view or the admin.

- `http://127.0.0.1:8000/podcast/ <http://127.0.0.1:8000/podcast/>`_
- `http://127.0.0.1:8000/admin/podcast/ <http://127.0.0.1:8000/admin/podcast/>`_
