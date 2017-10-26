from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, RedirectView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .feeds import ShowFeed
from .models import Enclosure, Episode, Show
from . import settings


class ShowListView(ListView):
    model = Show
    paginate_by = settings.PODCAST_PAGINATE_BY


class ShowDetailView(SingleObjectMixin, MultipleObjectMixin, TemplateView):
    paginate_by = settings.PODCAST_PAGINATE_BY
    template_name = 'podcast/show_detail.html'

    def get_object(self, queryset=None):
        if settings.PODCAST_SINGULAR:
            return get_object_or_404(Show, id=settings.PODCAST_ID)
        else:
            return get_object_or_404(Show, slug=self.kwargs['show_slug'])

    def get_queryset(self):
        """Return list with episode number attached to each episode."""
        queryset = self.get_object().episode_set.is_public()
        pub_list = list(queryset.order_by('pub_date'))
        for index, item in enumerate(pub_list):
            item.index = index + 1
        pub_list.reverse()
        return pub_list

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        return super(ShowDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ShowDetailView, self).get_context_data(**kwargs)
        context['episode_list'] = context['object_list']
        return context


class ShowFeedView(ShowDetailView):
    def get(self, request, *args, **kwargs):
        show = self.get_object()
        if show.going:
            return redirect(show.going, permanent=True)
        else:
            return ShowFeed()(request)


class EpisodeDetailView(DetailView):
    def get_object(self, queryset=None):
        """Return object with episode number attached to episode."""
        if settings.PODCAST_SINGULAR:
            show = get_object_or_404(Show, id=settings.PODCAST_ID)
        else:
            show = get_object_or_404(Show, slug=self.kwargs['show_slug'])
        episode = get_object_or_404(Episode.objects.is_public_or_secret(), show=show, slug=self.kwargs['slug'])
        index = Episode.objects.is_public_or_secret().filter(show=show, pub_date__lt=episode.pub_date).count()
        episode.index = index + 1
        episode.index_next = episode.index + 1
        episode.index_previous = episode.index - 1
        return episode


class EpisodeDownloadView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if settings.PODCAST_SINGULAR:
            show = get_object_or_404(Show, id=settings.PODCAST_ID)
        else:
            show = get_object_or_404(Show, slug=self.kwargs['show_slug'])
        episode = get_object_or_404(Episode.objects.is_public_or_secret(), show=show, slug=self.kwargs['slug'])
        try:
            enclosure = Enclosure.objects.get(episode=episode)
        except Enclosure.DoesNotExist:
            return None
        return enclosure.file.url
