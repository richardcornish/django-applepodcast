from __future__ import unicode_literals

import re

from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import add_domain
from django.template import TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _

from .. import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def show_url(context, **kwargs):
    """Return the show feed URL with different protocol."""
    if len(kwargs) != 2:
        raise TemplateSyntaxError(_('"show_url" tag takes exactly two keyword arguments.'))
    request = context['request']
    current_site = get_current_site(request)
    url = add_domain(current_site.domain, kwargs['url'])
    return re.sub(r'https?:\/\/', '%s://' % kwargs['protocol'], url)


@register.simple_tag
def get_podcast_singular():
    return settings.PODCAST_SINGULAR
