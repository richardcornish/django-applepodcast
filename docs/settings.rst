.. _settings:

Settings
********

The app offers several settings. By default, they are:

.. code-block:: python

   PODCAST_SINGULAR = True

   PODCAST_ID = 1

   PODCAST_EPISODE_LIMIT = None

   PODCAST_NO_ARTWORK = 'podcast/img/no_artwork.png'

   PODCAST_PAGINATE_BY = 10

   PODCAST_ALLOWED_TAGS = ['p', 'ol', 'ul', 'li', 'a', 'i', 'em', 'b', 'strong']


``PODCAST_SINGULAR``
====================

A boolean indicating display of multiple podcast shows.

The app displays a single show by default. If you would like to display multiple shows, set the ``PODCAST_SINGULAR`` variable in ``settings.py``.

.. code-block:: python

   PODCAST_SINGULAR = False

If you have multiple shows, you might want to edit the URL pattern in ``urls.py`` from ``podcast/`` to ``podcasts/``, although the difference is purely cosmetic.

.. code-block:: python

   from django.urls import include, path

   urlpatterns = [
       # ...
       path('podcasts/', include('podcast.urls')),
   ]

``PODCAST_ID``
==============

An integer indicating the primary key of the show to display; used when ``PODCAST_SINGULAR`` is ``True``. Concept modeled after the |SITE_ID|_ setting used in the `Sites <https://docs.djangoproject.com/en/2.0/ref/contrib/sites/>`_ application.

.. |SITE_ID| replace:: ``SITE_ID``
.. _SITE_ID: https://docs.djangoproject.com/en/2.0/ref/settings/#site-id

The app displays the first show by default.

``PODCAST_EPISODE_LIMIT``
=========================

An integer indicating the number of episodes to display in a show feed or ``None`` to display all episodes. Formerly the limit was an arbitrary 50 episodes.

The app displays all episodes in a show feed by default.

``PODCAST_NO_ARTWORK``
======================

A string indicating the path to an image used when artwork is lacking; used for shows, episodes, and video enclosures.

Although the path can be customized in the setting, you're probably better off overriding the image look up at the project level; that is, creating a new image at ``myproject/static/podcast/img/no_artwork.png``.

``PODCAST_PAGINATE_BY``
=======================

An integer indicating how many items to display in a list view or in a detail view of related objects; used for shows and episodes.

``PODCAST_ALLOWED_TAGS``
========================

A list indicating which HTML tags are allowed for display in output; used for show summaries and episode notes. The database can store HTML, but tags not specified in the list are stripped out, and the remaining output is wrapped in ``<![CDATA[...]]>`` tags. Uses the `Bleach <https://pypi.python.org/pypi/bleach>`_ Python package.

The list includes HTML tags specified in the `iOS 11 Apple Podcasts update <http://podcasts.apple.com/resources/spec/ApplePodcastsSpecUpdatesiOS11.pdf>`_ by default. The list also includes the conspicuously absent ``<li>`` and ``<strong>`` tags, which appear to be an oversight on Apple's part because ``<ol>``, ``<ul>``, and ``<b>`` are present in the original list. Note that the `specification <https://help.apple.com/itc/podcasts_connect/#/itcb54353390>`_ confusingly specifies a subset of fewer tags: ``<p>``, ``<ol>``, ``<ul>``, and ``<a>``.
