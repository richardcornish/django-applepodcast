from __future__ import unicode_literals

import os
import re
from collections import OrderedDict
from datetime import datetime
from xml.sax.saxutils import escape as _escape

from django.utils import timezone
from django.utils.text import slugify
from django.utils.xmlutils import SimplerXMLGenerator

try:
    from django.utils.xmlutils import UnserializableContentError
except ImportError:  # < Django 1.9
    class UnserializableContentError(ValueError):
        pass


class EscapeFriendlyXMLGenerator(SimplerXMLGenerator, object):
    """Subclass of Django's SimplerXMLGenerator.

    Django's addQuickElement() calls XMLGenerator.characters(), which in turn
    calls xml.sax.saxutils.escape(), which escapes characters too soon.
    This class allows unescaped characters to exist in XML elements.
    https://github.com/django/django/blob/2.0/django/utils/xmlutils.py
    https://docs.python.org/3/library/xml.sax.utils.html
    https://code.djangoproject.com/ticket/15936
    """

    def addQuickElement(self, name, contents=None, attrs=None, escape=True, cdata=False):
        """Convenience method for adding an element with no children."""
        if attrs is None:
            attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self.characters(contents, escape=escape, cdata=cdata)
        self.endElement(name)

    def characters(self, content, **kwargs):
        if content and re.search(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', content):
            # Fail loudly when content has control chars (unsupported in XML 1.0)
            # See http://www.w3.org/International/questions/qa-controls
            raise UnserializableContentError('Control characters are not supported in XML 1.0')
        # XMLGenerator.characters(self, content)

        # Python 3
        # https://github.com/python/cpython/blob/3.6/Lib/xml/sax/saxutils.py#L209
        try:
            if content:
                self._finish_pending_start_element()
                if not isinstance(content, str):
                    content = str(content, self._encoding)

        # Python 2
        # https://github.com/python/cpython/blob/2.7/Lib/xml/sax/saxutils.py#L185
        except AttributeError:
            if not isinstance(content, unicode):
                content = unicode(content, self._encoding)

        # Custom kwarg
        if kwargs['escape']:
            content = _escape(content)

        # Custom kwarg
        if kwargs['cdata']:
            content = '<![CDATA[%s]]>' % content

        self._write(content)

    def startElement(self, name, attrs):
        # Sort attrs for a deterministic output.
        sorted_attrs = OrderedDict(sorted(attrs.items())) if attrs else attrs
        try:
            super().startElement(name, sorted_attrs)
        except TypeError:
            super(EscapeFriendlyXMLGenerator, self).startElement(name, sorted_attrs)


def speaker_photo_path(instance, filename):
    name = re.sub(r"-", "_", slugify(instance.name))
    timestamp = datetime.strftime(timezone.now(), '%Y_%m_%d-%H_%M_%S')
    extension = os.path.splitext(filename)[1]
    return 'podcast/speakers/%s-%s%s' % (name, timestamp, extension)


def show_image_path(instance, filename):
    show = re.sub(r"-", "_", instance.slug)
    timestamp = datetime.strftime(timezone.now(), '%Y_%m_%d-%H_%M_%S')
    extension = os.path.splitext(filename)[1]
    return 'podcast/shows/%s-%s%s' % (show, timestamp, extension)


def episode_image_path(instance, filename):
    show = re.sub(r"-", "_", instance.show.slug)
    episode = re.sub(r"-", "_", instance.slug)
    timestamp = datetime.strftime(timezone.now(), '%Y_%m_%d-%H_%M_%S')
    extension = os.path.splitext(filename)[1]
    return 'podcast/episodes/%s-%s-%s%s' % (show, episode, timestamp, extension)


def enclosure_file_path(instance, filename):
    show = re.sub(r"-", "_", instance.episode.show.slug)
    episode = re.sub(r"-", "_", instance.episode.slug)
    timestamp = datetime.strftime(timezone.now(), '%Y_%m_%d-%H_%M_%S')
    extension = os.path.splitext(filename)[1]
    return 'podcast/enclosures/files/%s-%s-%s%s' % (show, episode, timestamp, extension)


def enclosure_poster_path(instance, filename):
    show = re.sub(r"-", "_", instance.episode.show.slug)
    episode = re.sub(r"-", "_", instance.episode.slug)
    timestamp = datetime.strftime(timezone.now(), '%Y_%m_%d-%H_%M_%S')
    extension = os.path.splitext(filename)[1]
    return 'podcast/enclosures/posters/%s-%s-%s%s' % (show, episode, timestamp, extension)
