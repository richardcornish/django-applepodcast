from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import Feed, add_domain
from django.utils import timezone
from django.utils.html import escape
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Show, Episode, Enclosure
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
        return attrs

    def add_root_elements(self, handler):
        super(ItunesFeed, self).add_root_elements(handler)
        handler.addQuickElement('copyright', self.feed['copyright'], escape=False, cdata=False)
        if self.feed['itunes']['subtitle']:
            handler.addQuickElement('itunes:subtitle', self.feed['itunes']['subtitle'], escape=False, cdata=True)
        if self.feed['itunes']['summary']:
            handler.addQuickElement('itunes:summary', self.feed['itunes']['summary'], escape=False, cdata=True)
        else:
            handler.addQuickElement('itunes:summary', self.feed['description'], escape=False, cdata=True)
        handler.addQuickElement('itunes:author', self.feed['itunes']['author']['name'])
        handler.startElement('itunes:owner', {})
        handler.addQuickElement('itunes:name', self.feed['itunes']['owner']['name'])
        handler.addQuickElement('itunes:email', self.feed['itunes']['owner']['email'])
        handler.endElement('itunes:owner')
        handler.addQuickElement('itunes:image', '', {'href': self.feed['itunes']['image']})
        for key, value in self.feed['itunes']['categories']:
            handler.startElement('itunes:category', {'text': key})
            for sub in value:
                handler.addQuickElement('itunes:category', '', {'text': sub})
            handler.endElement('itunes:category')
        handler.addQuickElement('itunes:explicit', self.feed['itunes']['explicit'])
        if self.feed['itunes']['block'] == 'yes':
            handler.addQuickElement('itunes:block', self.feed['itunes']['block'])
        if self.feed['itunes']['complete'] == 'yes':
            handler.addQuickElement('itunes:complete', self.feed['itunes']['complete'])

    def add_item_elements(self, handler, item):
        super(ItunesFeed, self).add_item_elements(handler, item)
        if item['itunes']['subtitle']:
            handler.addQuickElement('itunes:subtitle', item['itunes']['subtitle'], escape=False, cdata=True)
        if item['itunes']['summary']:
            handler.addQuickElement('itunes:summary', item['itunes']['summary'], escape=False, cdata=True)
        else:
            handler.addQuickElement('itunes:summary', item['description'], escape=False, cdata=True)
        if item['itunes']['author']['name']:
            handler.addQuickElement('itunes:author', item['itunes']['author']['name'])
        if item['itunes']['image']:
            handler.addQuickElement('itunes:image', '', {'href': item['itunes']['image']})
        handler.addQuickElement('itunes:explicit', item['itunes']['explicit'])
        if item['itunes']['block'] == 'yes':
            handler.addQuickElement('itunes:block', item['itunes']['block'])
        if item['itunes']['duration']:
            handler.addQuickElement('itunes:duration', item['itunes']['duration'])
        if item['itunes']['cc'] == 'yes':
            handler.addQuickElement('itunes:isClosedCaptioned', item['itunes']['cc'])


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

    def feed_extra_kwargs(self, obj):
        copyright = escape('%s & %s %s %s') % ('&#x2117;', '&#xA9;', timezone.now().year, escape(obj.copyright or obj.title))
        current_site = get_current_site(self.request)
        image_url = add_domain(current_site.domain, obj.get_image_url(), self.request.is_secure())
        return {
            'copyright': copyright,
            'itunes': {
                'subtitle': obj.subtitle,
                'summary': obj.summary,
                'author': {
                    'name': obj.author_name,
                    'email': obj.author_email,
                },
                'owner': {
                    'name': obj.owner_name or obj.author_name,
                    'email': obj.owner_email or obj.author_email,
                },
                'image': image_url,
                'categories': obj.get_categories_dict(),
                'explicit': obj.get_explicit(),
                'block': obj.get_block(),
                'complete': obj.get_complete(),
            }
        }

    def items(self, obj):
        return Episode.objects.filter(show=obj)[:settings.PODCAST_EPISODE_LIMIT]

    def item_title(self, item):
        return '%s' % item.title

    def item_description(self, item):
        return '%s' % item.description

    def item_guid(self, item):
        return self.item_enclosure_url(item)

    def item_pubdate(self, item):
        return item.pub_date

    def item_enclosure_url(self, item):
        try:
            current_site = get_current_site(self.request)
            enclosure_url = Enclosure.objects.get(episode=item).file.url
            return add_domain(current_site.domain, enclosure_url, self.request.is_secure())
        except Enclosure.DoesNotExist:
            return None

    def item_enclosure_length(self, item):
        try:
            return Enclosure.objects.get(episode=item).file.size
        except Enclosure.DoesNotExist:
            return None

    def item_enclosure_mime_type(self, item):
        try:
            return Enclosure.objects.get(episode=item).type
        except Enclosure.DoesNotExist:
            return None

    def item_extra_kwargs(self, item):
        current_site = get_current_site(self.request)
        image_url = item.image.url if item.image else item.show.get_image_url()
        image = add_domain(current_site.domain, image_url, self.request.is_secure())
        try:
            enclosure = Enclosure.objects.get(episode=item)
            cc = enclosure.get_cc()
            duration = enclosure.get_duration()
        except Enclosure.DoesNotExist:
            cc = None
            duration = None
        return {
            'itunes': {
                'subtitle': item.subtitle,
                'summary': item.summary,
                'author': {
                    'name': item.get_author_name(),
                    'email': item.get_author_email(),
                },
                'image': image,
                'explicit': item.get_explicit(),
                'block': item.get_block(),
                'cc': cc,
                'duration': duration,
            }
        }
