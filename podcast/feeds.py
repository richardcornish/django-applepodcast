from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import Feed, add_domain
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Enclosure, Episode, Show
from .utils import EscapeFriendlyXMLGenerator
from . import settings


class ItunesFeed(Rss201rev2Feed):
    def write(self, outfile, encoding):
        """Method override to create self-closing elements.

        https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.feedgenerator.SyndicationFeed.write
        https://github.com/django/django/blob/1.11/django/utils/feedgenerator.py#L242
        """
        try:
            handler = EscapeFriendlyXMLGenerator(outfile, encoding, short_empty_elements=True)
        except TypeError:  # Python 2
            handler = EscapeFriendlyXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement('rss', self.rss_attributes())
        handler.startElement('channel', self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement('rss')

    def rss_attributes(self):
        attrs = super(ItunesFeed, self).rss_attributes()
        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_root_elements(self, handler):
        super(ItunesFeed, self).add_root_elements(handler)
        handler.addQuickElement('copyright', self.feed['copyright'], escape=False, cdata=False)
        handler.addQuickElement('docs', self.feed['docs'])
        handler.startElement('image', {})
        handler.addQuickElement('url', self.feed['image'])
        handler.addQuickElement('title', self.feed['title'])
        handler.addQuickElement('link', self.feed['link'])
        handler.endElement('image')
        handler.addQuickElement('itunes:type', self.feed['itunes']['type'])
        handler.addQuickElement('itunes:subtitle', self.feed['itunes']['subtitle'])
        handler.addQuickElement('itunes:summary', self.feed['itunes']['summary'], escape=False, cdata=True)
        handler.addQuickElement('itunes:author', self.feed['itunes']['author']['name'])
        handler.startElement('itunes:owner', {})
        handler.addQuickElement('itunes:name', self.feed['itunes']['owner']['name'])
        handler.addQuickElement('itunes:email', self.feed['itunes']['owner']['email'])
        handler.endElement('itunes:owner')
        handler.addQuickElement('itunes:image', '', {'href': self.feed['image']})
        for key, value in self.feed['itunes']['categories']:
            handler.startElement('itunes:category', {'text': key})
            for sub in value:
                handler.addQuickElement('itunes:category', '', {'text': sub})
            handler.endElement('itunes:category')
        handler.addQuickElement('itunes:explicit', self.feed['itunes']['explicit'])
        handler.addQuickElement('itunes:block', self.feed['itunes']['block'])
        handler.addQuickElement('itunes:complete', self.feed['itunes']['complete'])
        if self.feed['itunes']['coming']:
            handler.addQuickElement('itunes:new-feed-url', self.feed['feed_url'])

    def add_item_elements(self, handler, item):
        super(ItunesFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('itunes:episodeType', item['itunes']['type'])
        handler.addQuickElement('itunes:title', item['itunes']['title'])
        handler.addQuickElement('itunes:summary', item['itunes']['summary'])
        handler.addQuickElement('content:encoded', item['itunes']['notes'], escape=False, cdata=True)
        handler.addQuickElement('itunes:author', item['itunes']['author']['name'])
        handler.addQuickElement('itunes:image', '', {'href': item['itunes']['image']})
        handler.addQuickElement('itunes:explicit', item['itunes']['explicit'])
        handler.addQuickElement('itunes:block', item['itunes']['block'])
        handler.addQuickElement('itunes:isClosedCaptioned', item['itunes']['cc'])
        if item['itunes']['season']:
            handler.addQuickElement('itunes:season', item['itunes']['season'])
        if item['itunes']['number']:
            handler.addQuickElement('itunes:episode', item['itunes']['number'])
        if item['itunes']['duration']:
            handler.addQuickElement('itunes:duration', item['itunes']['duration'])


class ShowFeed(Feed):
    feed_type = ItunesFeed

    def get_object(self, request, *args, **kwargs):
        self.request = request
        if settings.PODCAST_SINGULAR:
            return Show.objects.get(id=settings.PODCAST_ID)
        else:
            return Show.objects.get(slug=kwargs['show_slug'])

    def title(self, obj):
        return '%s' % obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return '%s' % obj.description

    def image(self, obj):
        current_site = get_current_site(self.request)
        return add_domain(current_site.domain, obj.get_image_url(), self.request.is_secure())

    def docs(self, obj):
        return 'http://blogs.law.harvard.edu/tech/rss'

    def feed_extra_kwargs(self, obj):
        return {
            'copyright': obj.get_copyright(),
            'image': self.image(obj),
            'docs': self.docs(obj),
            'itunes': {
                'type': obj.type,
                'subtitle': obj.get_subtitle(),
                'summary': obj.get_summary(),
                'author': {
                    'name': obj.author_name,
                    'email': obj.author_email,
                },
                'owner': {
                    'name': obj.get_owner_name(),
                    'email': obj.get_owner_email(),
                },
                'categories': obj.get_categories_dict(),
                'explicit': obj.get_explicit(),
                'block': obj.get_block(),
                'complete': obj.get_complete(),
                'coming': obj.coming,
            }
        }

    def items(self, obj):
        return Episode.objects.is_public().filter(show=obj)[:settings.PODCAST_EPISODE_LIMIT]

    def item_title(self, item):
        return '%s' % item.title

    def item_description(self, item):
        return '%s' % item.description

    def item_guid(self, item):
        return item.guid

    def item_guid_is_permalink(self, item):
        return False

    def item_pubdate(self, item):
        return item.pub_date

    def item_enclosure_url(self, item):
        current_site = get_current_site(self.request)
        enclosure_url = item.get_absolute_download_url()
        return add_domain(current_site.domain, enclosure_url, self.request.is_secure())

    def item_enclosure_length(self, item):
        try:
            enclosure = Enclosure.objects.get(episode=item)
        except Enclosure.DoesNotExist:
            return None
        return enclosure.file.size

    def item_enclosure_mime_type(self, item):
        try:
            enclosure = Enclosure.objects.get(episode=item)
        except Enclosure.DoesNotExist:
            return None
        return enclosure.type

    def item_image(self, item):
        current_site = get_current_site(self.request)
        return add_domain(current_site.domain, item.get_image_url(), self.request.is_secure())

    def item_cc(self, item):
        try:
            enclosure = Enclosure.objects.get(episode=item)
        except Enclosure.DoesNotExist:
            return None
        return enclosure.get_cc()

    def item_duration(self, item):
        try:
            enclosure = Enclosure.objects.get(episode=item)
        except Enclosure.DoesNotExist:
            return None
        return enclosure.get_duration()

    def item_extra_kwargs(self, item):
        return {
            'itunes': {
                'type': item.type,
                'season': item.get_season(),
                'number': item.get_number(),
                'title': item.get_title(),
                'summary': item.get_summary(),
                'notes': item.get_notes(),
                'author': {
                    'name': item.get_author_name(),
                    'email': item.get_author_email(),
                },
                'image': self.item_image(item),
                'explicit': item.get_explicit(),
                'block': item.get_block(),
                'cc': self.item_cc(item),
                'duration': self.item_duration(item),
            }
        }
