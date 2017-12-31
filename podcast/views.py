from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin

from .feeds import ShowFeed
from .models import Enclosure, Episode, Show
from . import settings


class ShowListView(ListView):
    model = Show
    paginate_by = settings.PODCAST_PAGINATE_BY


class ShowDetailView(MultipleObjectMixin, DetailView):
    paginate_by = settings.PODCAST_PAGINATE_BY

    def get_object(self, queryset=None):
        if settings.PODCAST_SINGULAR:
            return get_object_or_404(Show, id=settings.PODCAST_ID)
        else:
            return get_object_or_404(Show, slug=self.kwargs['show_slug'])

    def get_queryset(self):
        queryset = Episode.objects.is_public().filter(show=self.get_object())
        index = queryset.count()
        for obj in queryset:
            obj.index = index
            index -= 1
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ShowDetailView, self).get_context_data(**kwargs)
        context[self.object._meta.model_name] = self.object
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super(ShowDetailView, self).get(request, *args, **kwargs)


class ShowFeedView(ShowDetailView):
    def get(self, request, *args, **kwargs):
        show = self.get_object()
        feed = ShowFeed()
        return redirect(show.going, permanent=True) if show.going else feed(request)


class EpisodeDetailView(DetailView):
    def get_object(self, queryset=None):
        """Return object with episode number attached to episode."""
        if settings.PODCAST_SINGULAR:
            show = get_object_or_404(Show, id=settings.PODCAST_ID)
        else:
            show = get_object_or_404(Show, slug=self.kwargs['show_slug'])
        obj = get_object_or_404(Episode, show=show, slug=self.kwargs['slug'])
        index = Episode.objects.is_public_or_secret().filter(show=show, pub_date__lt=obj.pub_date).count()
        obj.index = index + 1
        obj.index_next = obj.index + 1
        obj.index_previous = obj.index -1
        return obj


class EpisodeDownloadView(EpisodeDetailView):
    def get(self, request, *args, **kwargs):
        episode = self.get_object()
        try:
            enclosure = Enclosure.objects.get(episode=episode)
        except Enclosure.DoesNotExist:
            return None
        return redirect(enclosure.file.url, permanent=False)
