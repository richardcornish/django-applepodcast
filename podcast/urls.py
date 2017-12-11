from __future__ import unicode_literals

try:
    from django.urls import include, re_path
except ImportError:
    from django.conf.urls import include, url as re_path

from .views import EpisodeDetailView, EpisodeDownloadView, ShowDetailView, ShowFeedView, ShowListView
from . import settings


app_name = 'podcast'

singular = [
    re_path(r'^feed/$', ShowFeedView.as_view(), name='show_feed'),
    re_path(r'^(?P<slug>[\w-]+)/download/$', EpisodeDownloadView.as_view(), name='episode_download'),
    re_path(r'^(?P<slug>[\w-]+)/$', EpisodeDetailView.as_view(), name='episode_detail'),
    re_path(r'^$', ShowDetailView.as_view(), name='show_detail'),
]

if settings.PODCAST_SINGULAR:
    urlpatterns = singular
else:
    urlpatterns = [
        re_path(r'^(?P<show_slug>[\w-]+)/', include(singular)),
        re_path(r'^$', ShowListView.as_view(), name='show_list'),
    ]
