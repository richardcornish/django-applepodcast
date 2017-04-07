from __future__ import unicode_literals

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .models import Show, Episode
from . import settings


class ShowListView(ListView):
    model = Show
    paginate_by = settings.PODCAST_PAGINATE_BY


class ShowDetailView(SingleObjectMixin, MultipleObjectMixin, TemplateView):
    paginate_by = settings.PODCAST_PAGINATE_BY
    template_name = 'podcast/show_detail.html'

    def get_object(self, queryset=None):
        if settings.PODCAST_SINGULAR:
            return Show.objects.get(id=settings.PODCAST_ID)
        else:
            return Show.objects.get(slug=self.kwargs['show_slug'])

    def get_queryset(self):
        """Return list with episode number attached to each episode."""
        queryset = self.get_object().episode_set.all()
        pub_list = list(queryset.order_by('pub_date'))
        for index, item in enumerate(pub_list):
            item.index = index + 1
        pub_list.reverse()
        return pub_list

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object_list = self.get_queryset()
        return super(ShowDetailView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ShowDetailView, self).get_context_data(**kwargs)
        context['episode_list'] = context['object_list']
        return context


class EpisodeDetailView(DetailView):
    def get_object(self, queryset=None):
        """Return object with episode number attached to episode."""
        if settings.PODCAST_SINGULAR:
            show = Show.objects.get(id=settings.PODCAST_ID)
        else:
            show = Show.objects.get(slug=self.kwargs['show_slug'])
        episode = Episode.objects.get(show=show, slug=self.kwargs['slug'])
        index = Episode.objects.filter(show=show, pub_date__lt=episode.pub_date).count()
        episode.index = index + 1
        episode.index_next = episode.index + 1
        episode.index_previous = episode.index - 1
        return episode
