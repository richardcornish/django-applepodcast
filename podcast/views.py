from __future__ import unicode_literals

try:
    from urllib.request import urlopen
except ImportError:  # Python 2
    from urllib2 import urlopen

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import add_domain
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
        context['podcast_singular'] = settings.PODCAST_SINGULAR
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

    def get_context_data(self, **kwargs):
        context = super(EpisodeDetailView, self).get_context_data(**kwargs)
        context['podcast_singular'] = settings.PODCAST_SINGULAR
        return context


class EpisodeDownloadView(EpisodeDetailView):
    def get(self, request, *args, **kwargs):
        episode = self.get_object()
        current_site = get_current_site(request)
        domain_url = add_domain(current_site.domain, episode.enclosure.file.url, self.request.is_secure())
        response = HttpResponse(urlopen(domain_url), content_type=episode.enclosure.type)
        response['Content-Disposition'] = 'attachment; filename="%s.%s%s"' % (episode.show.slug, episode.slug, episode.enclosure.get_extension())
        return response
