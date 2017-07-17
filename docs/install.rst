.. _install:

Install
*******

Install with the `pip <https://pip.pypa.io/en/stable/>`_ package manager.

.. code-block:: bash

   $ mkvirtualenv myvenv -p python3
   $ pip install django
   $ pip install django-applepodcast

After `creating a project <https://docs.djangoproject.com/en/1.11/intro/tutorial01/>`_, add ``podcast`` to ``INSTALLED_APPS`` in ``settings.py``.

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       'podcast',
   ]

Because the app is primarily model driven, you will want to expose the URL of the show's feed for submission to Apple Podcasts. Add the URL conf to ``urls.py``.

.. code-block:: python

   from django.conf.urls import url, include

   urlpatterns = [
       # ...
       url(r'^podcast/', include('podcast.urls')),
   ]

If you're on Django 1.8 or lower, you will need to add the ``namespace`` keyword argument to the ``include()`` method manually because the convenient ``app_name`` attribute in ``urls.py`` wasn't `added until Django 1.9 <https://docs.djangoproject.com/en/1.9/releases/1.9/#urls>`_.

.. code-block:: python

   from django.conf.urls import url, include

   urlpatterns = [
       # ...
       url(r'^podcast/', include('podcast.urls', namespace='podcast')),  # < Django 1.9
   ]

Add the models to your project by migrating the database.

.. code-block:: bash

   $ python manage.py migrate

Add the default `Apple Podcasts categories <https://help.apple.com/itc/podcasts_connect/#/itc9267a2f12>`_ by loading the fixtures.

.. code-block:: bash

   $ python manage.py loaddata podcast_category.json

Remember to update your ``requirements.txt`` file. In your project directory:

.. code-block:: bash

   $ pip freeze > requirements.txt
