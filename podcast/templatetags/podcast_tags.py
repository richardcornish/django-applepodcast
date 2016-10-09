from __future__ import unicode_literals

import re

from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import add_domain
from django.template import TemplateSyntaxError
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.simple_tag(takes_context=True)
def show_url(context, *args, **kwargs):
    """Return the show feed URL with different protocol."""
    if len(kwargs) != 2:
        raise TemplateSyntaxError(_('"show_url" tag takes exactly two keyword arguments.'))
    try:
        request = context['request']
    except IndexError:
        raise TemplateSyntaxError(_('"show_url" tag requires request in the template context. Add the request context processor to settings.'))
    current_site = get_current_site(request)
    url = add_domain(current_site.domain, kwargs['url'])
    return re.sub(r'https?:\/\/', '%s://' % kwargs['protocol'], url)
