from __future__ import unicode_literals

import os
import datetime

from django.test import TestCase, Client, override_settings
from django.utils import timezone

from ..models import Show, Episode, Enclosure

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


@override_settings(PODCAST_SINGULAR=False)
class PodcastTestCase(TestCase):
    fixtures = [
        'podcast_category.json',
    ]

    def setUp(self):
        super(PodcastTestCase, self).setUp()
        self.client = Client()

        # show
        show = Show.objects.create(
            title='All About Everything',
            slug='everything',
            description='All About Everything is a show about everything. Each week we dive into any subject known to man and talk about it as much as we can. Look for our podcast in the Podcasts app or in the iTunes Store',
            managing_editor='john.doe@example.com',
            webmaster='',
            ttl=60,
            subtitle='A show about everything',
            summary='',
            author_name='John Doe',
            author_email='',
            owner_name='John Doe',
            owner_email='john.doe@example.com',
            copyright='John Doe & Family',
            image='podcast/tests/static/everything/AllAboutEverything.jpg',
            explicit=False,
            block=False,
            complete=False,
        )
        show.categories.add(1, 4, 62, 63, 67)

        # episode 1
        episode_1 = Episode.objects.create(
            show=show,
            title='Shake Shake Shake Your Spices',
            slug='shake-shake-shake-your-spices',
            description='This week we talk about <a href="https://itunes/apple.com/us/book/antique-trader-salt-pepper/id429691295?mt=11">salt and pepper shakers</a>, comparing and contrasting pour rates, construction materials, and overall aesthetics. Come and join the party!',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2016-03-08T12:00:00', '%Y-%m-%dT%H:%M:%S')),
            summary='A short primer on table spices',
            image='podcast/tests/static/everything/AllAboutEverything/Episode1.jpg',
            explicit=False,
            block=False,
        )

        # episode 2
        episode_2 = Episode.objects.create(
            show=show,
            title='Socket Wrench Shootout',
            slug='socket-wrench-shootout',
            description='This week we talk about metric vs. Old English socket wrenches. Which one is better? Do you really need both? Get all of your answers here.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2016-03-09T18:00:00', '%Y-%m-%dT%H:%M:%S')),
            summary='Comparing socket wrenches is fun!',
            author_name='Jane Doe',
            image='podcast/tests/static/everything/AllAboutEverything/Episode2.jpg',
            explicit=False,
            block=False,
        )

        # episode 3
        episode_3 = Episode.objects.create(
            show=show,
            title='The Best Chili',
            slug='best-chili',
            description='This week we talk about the best Chili in the world. Which chili is better?',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2016-03-10T09:00:00', '%Y-%m-%dT%H:%M:%S')),
            summary='Jane and Eric',
            author_name='Jane Doe',
            image='podcast/tests/static/everything/AllAboutEverything/Episode3.jpg',
            explicit=False,
            block=False,
        )

        # episode 4
        episode_4 = Episode.objects.create(
            show=show,
            title='Red,Whine, & Blue',
            slug='red-whine-blue',
            description='This week we talk about surviving in a Red state if you are a Blue person. Or vice versa.',
            pub_date=timezone.make_aware(datetime.datetime.strptime('2016-03-10T22:15:00', '%Y-%m-%dT%H:%M:%S')),
            summary='Red + Blue != Purple',
            author_name='Various',
            image='podcast/tests/static/everything/AllAboutEverything/Episode4.jpg',
            explicit=False,
            block=False,
        )

        # enclosure 1
        Enclosure.objects.create(
            episode=episode_1,
            file='podcast/tests/static/everything/AllAboutEverythingEpisode3.m4a',
            type='audio/x-m4a',
            cc=False,
        )

        # enclosure 2
        Enclosure.objects.create(
            episode=episode_2,
            file='podcast/tests/static/everything/AllAboutEverythingEpisode2.mp4',
            type='video/mp4',
            cc=False,
        )

        # enclosure 3
        Enclosure.objects.create(
            episode=episode_3,
            file='podcast/tests/static/everything/AllAboutEverythingEpisode2.m4v',
            type='video/x-m4v',
            cc=True,
        )

        # enclosure 4
        Enclosure.objects.create(
            episode=episode_4,
            file='podcast/tests/static/everything/AllAboutEverythingEpisode4.mp3',
            type='audio/mpeg',
            cc=False,
        )

    def test_show_feed(self):
        response = self.client.get(reverse('podcast:show_feed'))
        with open(os.path.join(os.path.dirname(__file__), 'feed.xml'), 'r') as file_1:
            xml_1 = file_1.read()
            xml_2 = response.content.decode('utf-8').replace('http://testserverpodcast', 'http://testserver/podcast')
            self.maxDiff = None
            self.assertXMLEqual(xml_1, xml_2)
