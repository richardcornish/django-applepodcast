from __future__ import unicode_literals

from django.views.generic import ListView, DetailView

from .models import Show, Episode
from .mixins import PodcastSingularMixin, RelatedPaginatorMixin, EnclosureDownloadMixin
from . import settings


class ShowListView(ListView):
    model = Show
    paginate_by = settings.PODCAST_PAGINATE_BY


class ShowDetailView(PodcastSingularMixin, RelatedPaginatorMixin, DetailView):
    def get_object(self, queryset=None):
        if settings.PODCAST_SINGULAR:
            return Show.objects.get(id=settings.PODCAST_ID)
        else:
            return Show.objects.get(slug=self.kwargs['show_slug'])

    def get_related_objects(self):
        return self.get_object().episode_set.all()


class EpisodeDetailView(PodcastSingularMixin, DetailView):
    def get_object(self, queryset=None):
        if settings.PODCAST_SINGULAR:
            show = Show.objects.get(id=settings.PODCAST_ID)
            return Episode.objects.get(show=show, slug=self.kwargs['slug'])
        else:
            return Episode.objects.get(show__slug=self.kwargs['show_slug'], slug=self.kwargs['slug'])


class EpisodeDownloadView(EnclosureDownloadMixin, EpisodeDetailView):
    pass
