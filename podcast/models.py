from __future__ import division
from __future__ import unicode_literals

import os
from ast import literal_eval
from datetime import timedelta

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

from . import settings


@python_2_unicode_compatible
class Speaker(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("E-mail"), unique=True)
    photo = models.ImageField(_("Photo"), upload_to="podcast/speakers/", blank=True)
    bio = models.TextField(_("Bio"), blank=True)

    class Meta:
        ordering = ["name", "email"]
        verbose_name = _("speaker")
        verbose_name_plural = _("speakers")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Category(models.Model):
    parent = models.ForeignKey("self", verbose_name=_("parent"), related_name=_("children"), null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True)
    full = models.CharField(_("full title"), max_length=255, editable=False)
    json = models.TextField(_("JSON"), editable=False)

    class Meta:
        ordering = ["full"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.get_full(self)

    def save(self, *args, **kwargs):
        self.full = self.get_full(self)
        self.json = self.get_json(self)
        super(Category, self).save(*args, **kwargs)

    def get_full(self, object):
        if object.parent is None:
            return object.title
        else:
            return "%s / %s" % (self.get_full(object.parent), object.title)

    def get_json(self, object, children=False):
        if object.parent is None:
            if not children:
                return '{"%s": []}' % object.title
            else:
                return "%s" % object.title
        else:
            return '{"%s": ["%s"]}' % (self.get_json(object.parent, children=True), object.title)


@python_2_unicode_compatible
class Show(models.Model):
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True)
    image = models.ImageField(_("image"), upload_to="podcast/shows/", blank=True, help_text=_("1400&times;1400&ndash;3000&times;3000px; 72DPI; JPG, PNG; RGB; if blank, default <a href=\"%s\">no artwork</a> is used") % staticfiles_storage.url(settings.PODCAST_NO_ARTWORK))
    description = models.TextField(_("description"), help_text=_("Accepts HTML"))
    subtitle = models.CharField(_("subtitle"), max_length=255, help_text=_("Accepts HTML"))
    summary = models.TextField(_("summary"), blank=True, max_length=4000, help_text=_("Max length of 4,000 characters; accepts HTML; if blank, uses show's description"))
    author_name = models.CharField(_("author name"), max_length=255, help_text=_("Appears as the \"artist\" of the podcast"))
    author_email = models.EmailField(_("author e-mail"))
    owner_name = models.CharField(_("owner name"), max_length=255, blank=True, help_text=_("Administrative contact of the podcast; if blank, uses author name"))
    owner_email = models.EmailField(_("owner e-mail"), blank=True, max_length=255, help_text=_("Administrative contact of the podcast; if blank, uses author email"))
    copyright = models.CharField(_("copyright"), max_length=255, blank=True, help_text=_("Organization name; &copy; and %s will be prepended automatically; if blank, uses show's title" % timezone.now().year))
    categories = models.ManyToManyField(Category, verbose_name=_("categories"), help_text=_("Please select parent category if selecting a subcategory, e.g. <strong>Arts</strong> if <strong>Arts / Design</strong>"))
    explicit = models.BooleanField(_("explicit?"), default=False, help_text=_("Indicates explicit language or adult content"))
    block = models.BooleanField(_("block?"), default=False, help_text=_("Prevents entire podcast from appearing on the iTunes Store"))
    complete = models.BooleanField(_("complete?"), default=False, help_text=_("Indicates entire podcast is complete and no future episodes will be created"))
    itunes = models.URLField(_("iTunes URL"), blank=True, help_text=_("Paste iTunes URL here after <a href=\"https://podcastsconnect.apple.com/\">submission of show feed URL</a> to Podcasts Connect"))
    hosts = models.ManyToManyField(Speaker, verbose_name=_("hosts"), blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name = _("show")
        verbose_name_plural = _("shows")

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        if settings.PODCAST_SINGULAR:
            return reverse("podcast:show_detail")
        else:
            return reverse("podcast:show_detail", args=[self.slug])

    def get_absolute_feed_url(self):
        if settings.PODCAST_SINGULAR:
            return reverse("podcast:show_feed")
        else:
            return reverse("podcast:show_feed", args=[self.slug])

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return staticfiles_storage.url(settings.PODCAST_NO_ARTWORK)

    def get_categories_dict(self):
        old_dicts = [literal_eval(c.json) for c in self.categories.all()]
        new_dict = {}
        for old_dict in old_dicts:
            try:
                for key, value in old_dict.iteritems():
                    if key not in new_dict:
                        new_dict[key] = value
                    else:
                        for sub in value:
                            new_dict[key].append(sub)
            except AttributeError:  # Python 3
                for key, value in old_dict.items():
                    if key not in new_dict:
                        new_dict[key] = value
                    else:
                        for sub in value:
                            new_dict[key].append(sub)
        try:
            return sorted(new_dict.iteritems())
        except AttributeError:  # Python 3
            return sorted(new_dict.items())

    def get_explicit(self):
        return "yes" if self.explicit else "no"

    def get_block(self):
        return "yes" if self.block else "no"

    def get_complete(self):
        return "yes" if self.complete else "no"

    def get_latest_duration(self):
        episode = self.episode_set.all().first()
        return episode.enclosure.get_duration() if episode else ""
    get_latest_duration.short_description = _("last episode duration")

    def get_latest_pub_date(self):
        episode = self.episode_set.all().first()
        return episode.pub_date if episode else ""
    get_latest_pub_date.short_description = _("last episode pub date")


@python_2_unicode_compatible
class Episode(models.Model):
    show = models.ForeignKey(Show, verbose_name=_("show"))
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"),)
    description = models.TextField(_("description"), help_text=_("Accepts HTML"))
    pub_date = models.DateTimeField(_("pub date"),)
    subtitle = models.CharField(_("subtitle"), max_length=255, blank=True, help_text=_("Accepts HTML"))
    summary = models.TextField(_("summary"), blank=True, max_length=4000, help_text=_("Max length of 4,000 characters; accepts HTML; if blank, uses description"))
    author_name = models.CharField(_("author name"), max_length=255, blank=True, help_text=_("Appears as the \"artist\" of the episode; if blank, uses show's author name"))
    author_email = models.EmailField(_("author e-mail"), blank=True, help_text=_("If blank, uses show's author email"))
    image = models.ImageField(_("image"), upload_to="podcast/episodes/", blank=True, help_text=_("1400&times;1400&ndash;3000&times;3000px, 72DPI, JPG/PNG, RGB; if blank, uses show's image"))
    explicit = models.BooleanField(_("explicit?"), default=False, help_text=_("Indicates explicit language or adult content"))
    block = models.BooleanField(_("block?"), default=False, help_text=_("Prevents episode from appearing on the iTunes Store"))
    hosts = models.ManyToManyField(Speaker, verbose_name=_("hosts"), related_name="host", blank=True, help_text=_("If different from show hosts"))
    guests = models.ManyToManyField(Speaker, verbose_name=_("guests"), related_name="guest", blank=True)

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = _("episode")
        verbose_name_plural = _("episodes")

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        if settings.PODCAST_SINGULAR:
            return reverse("podcast:episode_detail", args=[self.slug])
        else:
            return reverse("podcast:episode_detail", args=[self.show.slug, self.slug])

    def validate_unique(self, exclude=None):
        """Episode slugs don't need to be unique *unless* in the same show."""
        if Episode.objects.filter(show=self.show, slug=self.slug).count() > 1:
            raise ValidationError(_("Episode titles must be unique within the same show."))
        super(Episode, self).validate_unique(exclude=None)

    def get_author_name(self):
        return self.author_name if self.author_name else self.show.author_name

    def get_author_email(self):
        return self.author_email if self.author_email else self.show.author_email

    def get_explicit(self):
        return "yes" if self.explicit else "no"

    def get_block(self):
        return "yes" if self.block else "no"

    def get_previous(self):
        return self.get_previous_by_pub_date(show=self.show)

    def get_next(self):
        return self.get_next_by_pub_date(show=self.show)

    def get_duration(self):
        return self.enclosure.get_duration()
    get_duration.short_description = _("duration")


@python_2_unicode_compatible
class Enclosure(models.Model):
    TYPE_CHOICES = (
        ("audio/mpeg", _("MP3 audio")),
        ("audio/x-m4a", _("M4A audio")),
        ("video/mp4", _("MP4 video")),
        ("video/x-m4v", _("M4V video")),
        ("video/quicktime", _("MOV video")),
        ("application/pdf", _("PDF file")),
        ("document/x-epub", _("ePub file")),
    )
    episode = models.OneToOneField(Episode, verbose_name=_("episode"))
    file = models.FileField(_("file"), upload_to="podcast/enclosures/files/", help_text=_("Supported formats: M4A, MP3, MOV, MP4, M4V, PDF, and EPUB"))
    timedelta = models.DurationField(_("time delta"), null=True)
    type = models.CharField(_("type"), max_length=255, choices=TYPE_CHOICES, default="audio/mpeg")
    poster = models.ImageField(_("poster"), upload_to="podcast/enclosures/posters/", blank=True, help_text=_("For video files"))
    cc = models.BooleanField(_("closed captions?"), default=False, help_text=_("For video files with closed captions"))

    class Meta:
        ordering = ["-episode__pub_date"]
        verbose_name = _("enclosure")
        verbose_name_plural = _("enclosures")

    def __str__(self):
        return "%s: %s" % (self.episode, self.type)

    def save(self, *args, **kwargs):
        if self.type == "audio/mpeg":
            media = MP3(self.file)
        elif self.type == "audio/x-m4a" or \
                self.type == "video/mp4" or \
                self.type == "video/x-m4v" or \
                self.type == "video/quicktime":
                media = MP4(self.file)
        self.timedelta = timedelta(seconds=int(media.info.length))
        super(Enclosure, self).save(*args, **kwargs)

    def get_poster_url(self):
        if self.poster:
            return self.poster.url
        elif self.episode.image:
            return self.episode.image.url
        else:
            return staticfiles_storage.url(settings.PODCAST_NO_ARTWORK)

    def get_cc(self):
        return "yes" if self.cc else "no"

    def get_megabytes(self):
        return "%.1f" % (self.file.size / 1048576)

    def get_extension(self):
        return os.path.splitext(self.file.url)[1]

    def get_duration(self):
        if self.timedelta:
            m, s = divmod(self.timedelta.total_seconds(), 60)
            h, m = divmod(m, 60)
            if h:
                return "%02d:%02d:%02d" % (h, m, s)
            else:
                return "%02d:%02d" % (m, s)
        else:
            return None
    get_duration.short_description = _("duration")
