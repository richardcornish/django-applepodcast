from __future__ import unicode_literals

from django.http import HttpResponse
from django.test import TestCase, Client

from ..models import Show, Episode, Enclosure
from .export import FEED_EXPORT


class PodcastTestCase(TestCase):
    fixtures = [
        'podcast_category.json',
        'tests/podcast_show.json',
        'tests/podcast_episode.json',
        'tests/podcast_enclosure.json',
    ]

    def setUp(self):
        super(PodcastTestCase, self).setUp()
        self.show = Show.objects.get(pk=1)
        self.episode = Episode.objects.get(pk=1)
        self.enclosure = Enclosure.objects.get(pk=1)

    def test_duration_of_enclosure(self):
        self.assertEqual(self.enclosure.get_duration(), '53:31')
