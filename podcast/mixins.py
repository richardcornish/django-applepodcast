from __future__ import unicode_literals

from . import settings


class PodcastSingularMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PodcastSingularMixin, self).get_context_data(**kwargs)
        context['podcast_singular'] = settings.PODCAST_SINGULAR
        return context
