from __future__ import unicode_literals

from django.conf import settings


PODCAST_SINGULAR = getattr(settings, 'PODCAST_SINGULAR', True)

PODCAST_ID = getattr(settings, 'PODCAST_ID', 1)

PODCAST_EPISODE_LIMIT = getattr(settings, 'PODCAST_EPISODE_LIMIT', None)

PODCAST_NO_ARTWORK = getattr(settings, 'PODCAST_NO_ARTWORK', 'podcast/img/no_artwork.png')

PODCAST_PAGINATE_BY = getattr(settings, 'PODCAST_PAGINATE_BY', 10)

PODCAST_ALLOWED_TAGS = getattr(settings, 'PODCAST_ALLOWED_TAGS', [
    'p', 'ol', 'ul', 'li', 'a', 'i', 'em', 'b', 'strong'
])
