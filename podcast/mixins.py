from __future__ import unicode_literals

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen  # Python 2

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import add_domain
from django.core.paginator import Paginator

from . import settings


class PodcastSingularMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PodcastSingularMixin, self).get_context_data(**kwargs)
        context['podcast_singular'] = settings.PODCAST_SINGULAR
        return context


class RelatedPaginatorMixin(object):
    paginate_by = settings.PODCAST_PAGINATE_BY

    def get_context_data(self, **kwargs):
        object_list = self.get_related_objects()
        if hasattr(object_list, 'model'):
            context_object_name = '%s_list' % object_list.model._meta.model_name
        context = super(RelatedPaginatorMixin, self).get_context_data(**kwargs)
        context[context_object_name] = Paginator(
            object_list,
            self.paginate_by
        ).page(self.request.GET.get('page', '1'))
        return context


class EnclosureDownloadMixin(object):
    def get(self, request, *args, **kwargs):
        episode = self.get_object()
        current_site = get_current_site(request)
        domain_url = add_domain(current_site.domain, episode.enclosure.file.url, self.request.is_secure())
        response = HttpResponse(urlopen(domain_url), content_type=episode.enclosure.type)
        response['Content-Disposition'] = 'attachment; filename="%s.%s%s"' % (episode.show.slug, episode.slug, episode.enclosure.get_extension())
        return response
