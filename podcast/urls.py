from __future__ import unicode_literals

from django.conf.urls import url, include

from .views import EpisodeDetailView, EpisodeDownloadView, ShowDetailView, ShowFeedView, ShowListView
from . import settings


app_name = 'podcast'

singular = [
    url(r'^feed/$', ShowFeedView.as_view(), name='show_feed'),
    url(r'^(?P<slug>[\w-]+)/download/$', EpisodeDownloadView.as_view(), name='episode_download'),
    url(r'^(?P<slug>[\w-]+)/$', EpisodeDetailView.as_view(), name='episode_detail'),
    url(r'^$', ShowDetailView.as_view(), name='show_detail'),
]

if settings.PODCAST_SINGULAR:
    urlpatterns = singular
else:
    urlpatterns = [
        url(r'^(?P<show_slug>[\w-]+)/', include(singular)),
        url(r'^$', ShowListView.as_view(), name='show_list'),
    ]
