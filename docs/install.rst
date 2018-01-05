.. _install:

Install
*******

Install with `Pipenv <https://docs.pipenv.org/>`_.

.. code-block:: bash

   $ pipenv install django django-applepodcast

After `creating a project <https://docs.djangoproject.com/en/2.0/intro/tutorial01/>`_, add ``podcast`` to ``INSTALLED_APPS`` in ``settings.py``.

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       'podcast',
   ]

Because the app is primarily model driven, you will want to expose the URL of the show's feed for submission to Apple Podcasts. `Add the URL conf <https://docs.djangoproject.com/en/2.0/topics/http/urls/#including-other-urlconfs>`_ to ``urls.py``.

.. code-block:: python

   from django.urls import include, path

   urlpatterns = [
       # ...
       path('podcast/', include('podcast.urls')),
   ]

If you're on Django 1.11, 1.10, or 1.9, use the older, `regex-based syntax <https://docs.djangoproject.com/en/1.11/topics/http/urls/#including-other-urlconfs>`_ instead.

.. code-block:: python

   from django.conf.urls import include, url

   urlpatterns = [
       # ...
       url(r'^podcast/', include('podcast.urls')),
   ]

If you're on Django 1.8, you will `additionally <https://docs.djangoproject.com/en/1.8/topics/http/urls/#url-namespaces-and-included-urlconfs>`_ need to add the ``namespace`` keyword argument to the ``include()`` method manually because the convenient ``app_name`` attribute in ``urls.py`` wasn't `added until Django 1.9 <https://docs.djangoproject.com/en/1.9/releases/1.9/#urls>`_.

.. code-block:: python

   from django.conf.urls import include, url

   urlpatterns = [
       # ...
       url(r'^podcast/', include('podcast.urls', namespace='podcast')),
   ]

Add the models to your project by migrating the database.

.. code-block:: bash

   $ pipenv run python manage.py migrate

Add the default `Apple Podcasts categories <https://help.apple.com/itc/podcasts_connect/#/itc9267a2f12>`_ by loading the fixtures.

.. code-block:: bash

   $ pipenv run python manage.py loaddata podcast_category.json
