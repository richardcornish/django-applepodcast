from __future__ import division
from __future__ import unicode_literals

import hashlib
from ast import literal_eval
from datetime import timedelta

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import bleach
import mutagen

from .managers import EpisodeManager
from .utils import enclosure_file_path, enclosure_poster_path, episode_image_path, show_image_path, speaker_photo_path
from . import settings

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


@python_2_unicode_compatible
class Speaker(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("E-mail"), unique=True)
    photo = models.ImageField(_("Photo"), upload_to=speaker_photo_path, blank=True)
    bio = models.TextField(_("Bio"), blank=True)

    class Meta:
        ordering = ["name", "email"]
        verbose_name = _("speaker")
        verbose_name_plural = _("speakers")

    def __str__(self):
        return "%s" % self.name


@python_2_unicode_compatible
class Category(models.Model):
    parent = models.ForeignKey("self", verbose_name=_("parent"), related_name=_("children"), null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True)
    full = models.CharField(_("full title"), max_length=255, editable=False)

    class Meta:
        ordering = ["full"]
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return "%s" % self.get_str(self)

    def save(self, *args, **kwargs):
        self.full = self.get_str(self)
        super(Category, self).save(*args, **kwargs)

    def get_str(self, obj, delimiter=" | ", trail=""):
        delimiter = delimiter if trail else ""
        if obj.parent:
            return self.get_str(obj.parent, trail="%s%s%s" % (obj.title, delimiter, trail))
        else:
            return "%s%s%s" % (obj.title, delimiter, trail)


@python_2_unicode_compatible
class Show(models.Model):
    TYPE_CHOICES = (
        ("episodic", _("Episodic")),
        ("serial", _("Serial")),
    )
    type = models.CharField(_("type"), max_length=255, choices=TYPE_CHOICES, default="episodic", help_text=_("Episodic presents episodes by latest, serial presents episodes by episode number; both support seasons"))
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True)
    image = models.ImageField(_("image"), upload_to=show_image_path, blank=True, help_text=_("1400&times;1400&ndash;3000&times;3000px; 72DPI; JPG, PNG; RGB; if blank, default <a href=\"%s\">no artwork</a> is used") % staticfiles_storage.url(settings.PODCAST_NO_ARTWORK))
    description = models.TextField(_("description"), help_text=_("Accepts HTML"))
    managing_editor = models.EmailField(_("editor e-mail"), max_length=255, default="", help_text=_("E-mail of administrative contact"))
    webmaster = models.EmailField(_("webmaster e-mail"), max_length=255, blank=True, help_text=_("E-mail of technical contact; if blank, uses editor e-mail"))
    ttl = models.PositiveIntegerField(_("TTL"), default=60, help_text=_("Time to live; minutes until cached feed refreshed"))
    subtitle = models.CharField(_("subtitle"), max_length=255, help_text=_("A single, descriptive sentence of the show"))
    summary = models.TextField(_("summary"), blank=True, max_length=4000, help_text=_("Max length of 4,000 characters; accepts HTML; if blank, uses show's description"))
    author_name = models.CharField(_("author name"), max_length=255, blank=True, help_text=_("Name of \"artist\" of the podcast; if blank, uses show title"))
    author_email = models.EmailField(_("author e-mail"), blank=True, help_text=_("E-mail of administrative contact; if blank, uses editor e-mail"))
    owner_name = models.CharField(_("owner name"), max_length=255, blank=True, help_text=_("Name of technical contact; if blank, uses show title"))
    owner_email = models.EmailField(_("owner e-mail"), blank=True, help_text=_("E-mail of technical contact; if blank, uses webmaster e-mail"))
    copyright = models.CharField(_("copyright"), max_length=255, blank=True, help_text=_("Organization name; &copy; and %s will be prepended automatically; if blank, uses show's title" % timezone.now().year))
    categories = models.ManyToManyField(Category, verbose_name=_("categories"), help_text=_("Please select parent category if selecting a subcategory, e.g. <strong>Arts</strong> if <strong>Arts / Design</strong>"))
    explicit = models.BooleanField(_("explicit?"), default=False, help_text=_("Indicates explicit language or adult content"))
    block = models.BooleanField(_("block?"), default=False, help_text=_("Prevents entire podcast from appearing on Apple Podcasts"))
    complete = models.BooleanField(_("complete?"), default=False, help_text=_("Indicates entire podcast is complete and no future episodes will be created"))
    apple = models.URLField(_("Apple Podcasts URL"), blank=True, help_text=_("Paste Apple Podcasts URL here after submission of show feed URL to <a href=\"https://podcastsconnect.apple.com/\">Podcasts Connect</a>"))
    coming = models.BooleanField(_("coming"), default=False, help_text=_("Indicates whether users are coming from an old feed; if set, leave for four weeks; see <a href=\"https://help.apple.com/itc/podcasts_connect/#/itca489031e0\">documentation</a>"))
    going = models.URLField(_("going"), blank=True, help_text=_("Permanently redirect users to URL of a new feed; see <a href=\"https://help.apple.com/itc/podcasts_connect/#/itca489031e0\">documentation</a>"))
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
        return self.image.url if self.image else staticfiles_storage.url(settings.PODCAST_NO_ARTWORK)

    def get_ttl(self):
        return str(self.ttl) if self.ttl else ""

    def get_subtitle(self):
        text = self.subtitle
        tags = []
        return bleach.clean(text, tags=tags, strip=True)

    def get_summary(self):
        text = self.summary if self.summary else self.description
        tags = settings.PODCAST_ALLOWED_TAGS
        return bleach.clean(text, tags=tags, strip=True)

    def get_webmaster(self):
        return self.webmaster if self.webmaster else self.managing_editor

    def get_author_name(self):
        return self.author_name if self.author_name else self.title

    def get_author_email(self):
        return self.author_email if self.author_email else self.managing_editor

    def get_owner_name(self):
        return self.owner_name if self.owner_name else self.title

    def get_owner_email(self):
        return self.owner_email if self.owner_email else self.get_webmaster()

    def get_category(self, obj, trail={}):
        if obj.parent:
            return self.get_category(obj.parent, trail={obj.title: trail})
        else:
            return {obj.title: trail}

    def get_categories(self):
        # Apple Podcasts-friendly categories; i.e. not recursive
        # e.g.: {'Arts': ['Food'], 'TV & Film': [], 'Technology': ['Gadgets']}
        categories = {}
        for item in [self.get_category(obj) for obj in self.categories.all()]:
            for key in item:
                if not key in categories:
                    categories[key] = []
                else:
                    for k in item[key]:
                        categories[key].append(k)
        return categories

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
    STATUS_CHOICES = (
        ("public", _("Public")),
        ("secret", _("Secret")),
        ("private", _("Private")),
    )
    TYPE_CHOICES = (
        ("full", _("Full")),
        ("trailer", _("Trailer")),
        ("bonus", _("Bonus")),
    )
    show = models.ForeignKey(Show, verbose_name=_("show"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"),)
    description = models.TextField(_("description"), help_text=_("Accepts HTML"))
    pub_date = models.DateTimeField(_("pub date"), help_text=_("If in future, episode hidden until date arrives (unless status is secret)"))
    status = models.CharField(_("status"), max_length=255, choices=STATUS_CHOICES, default="public", help_text=_("Public is openly visible; secret is visibile but unlisted; private is not visible"))
    type = models.CharField(_("type"), max_length=255, choices=TYPE_CHOICES, default="full", help_text=_("Full is for episodes, trailer is for promotional previews, and bonus is for extra content"))
    season = models.PositiveIntegerField(_("season"), null=True, blank=True, help_text=_("If a serialized show, number of the season"))
    number = models.PositiveIntegerField(_("number"), null=True, blank=True, help_text=_("If a serialized show, number of the episode within the season"))
    itunes_title = models.CharField(_("title"), max_length=255, blank=True, help_text=_("Do not specify show title, episode number, or season number; if blank, uses original title"))
    summary = models.CharField(_("summary"), max_length=255, blank=True, help_text=_("A single, descriptive sentence of the episode"))
    notes = models.TextField(_("notes"), blank=True, max_length=4000, help_text=_("Max length of 4,000 characters; accepts &lt;p&gt; &lt;ol&gt; &lt;ul&gt; &lt;li&gt; &lt;a&gt; &lt;em&gt; &lt;i&gt; &lt;b&gt; &lt;strong&gt;; if blank, uses description"))
    author_name = models.CharField(_("author name"), max_length=255, blank=True, help_text=_("Appears as the \"artist\" of the episode; if blank, uses show's author name"))
    author_email = models.EmailField(_("author e-mail"), blank=True, help_text=_("If blank, uses show's author email"))
    image = models.ImageField(_("image"), upload_to=episode_image_path, blank=True, help_text=_("1400&times;1400&ndash;3000&times;3000px, 72DPI, JPG/PNG, RGB; if blank, uses show's image"))
    explicit = models.BooleanField(_("explicit?"), default=False, help_text=_("Indicates explicit language or adult content"))
    block = models.BooleanField(_("block?"), default=False, help_text=_("Prevents episode from appearing on Apple Podcasts"))
    hosts = models.ManyToManyField(Speaker, verbose_name=_("hosts"), related_name="host", blank=True, help_text=_("If different from show hosts"))
    guests = models.ManyToManyField(Speaker, verbose_name=_("guests"), related_name="guest", blank=True)
    guid = models.CharField(_("GUID"), max_length=64, editable=False)

    objects = EpisodeManager()

    class Meta:
        ordering = ["-pub_date", "-id"]
        verbose_name = _("episode")
        verbose_name_plural = _("episodes")

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        # Save instance now to obtain object ID
        super(Episode, self).save(*args, **kwargs)
        # Save unique but reproducible hash of object ID
        if not self.guid:
            bytes_id = force_bytes(self.id)
            self.guid = hashlib.sha256(bytes_id).hexdigest()
            self.save(update_fields=["guid"])

    def get_absolute_url(self):
        if settings.PODCAST_SINGULAR:
            return reverse("podcast:episode_detail", args=[self.slug])
        else:
            return reverse("podcast:episode_detail", args=[self.show.slug, self.slug])

    def get_absolute_download_url(self):
        if settings.PODCAST_SINGULAR:
            return reverse("podcast:episode_download", args=[self.slug])
        else:
            return reverse("podcast:episode_download", args=[self.show.slug, self.slug])

    def validate_unique(self, exclude=None):
        # Episode slugs don't need to be unique *unless* in the same show.
        if Episode.objects.filter(show=self.show, slug=self.slug).count() > 1:
            raise ValidationError(_("Episode titles must be unique within the same show."))
        super(Episode, self).validate_unique(exclude=None)

    def get_season(self):
        return str(self.season) if self.season else ""

    def get_number(self):
        return str(self.number) if self.number else ""

    def get_title(self):
        return self.itunes_title if self.itunes_title else self.title

    def get_summary(self):
        text = self.summary
        tags = []
        return bleach.clean(text, tags=tags, strip=True)

    def get_notes(self):
        text = self.notes if self.notes else self.description
        tags = settings.PODCAST_ALLOWED_TAGS
        return bleach.clean(text, tags=tags, strip=True)

    def get_author_name(self):
        return self.author_name if self.author_name else self.show.get_author_name()

    def get_author_email(self):
        return self.author_email if self.author_email else self.show.get_author_email()

    def get_image_url(self):
        return self.image.url if self.image else self.show.get_image_url()

    def get_explicit(self):
        return "yes" if self.explicit else "no"

    def get_block(self):
        return "yes" if self.block else "no"

    def get_previous(self):
        return self.get_previous_by_pub_date(show=self.show, status="public", pub_date__lte=timezone.now())

    def get_next(self):
        return self.get_next_by_pub_date(show=self.show, status="public", pub_date__lte=timezone.now())

    def get_duration(self):
        return self.enclosure.get_duration()
    get_duration.short_description = _("duration")

    def is_public(self):
        return self.status == "public"

    def is_secret(self):
        return self.status == "secret"

    def is_private(self):
        return self.status == "private"


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
    episode = models.OneToOneField(Episode, verbose_name=_("episode"), on_delete=models.CASCADE)
    file = models.FileField(_("file"), upload_to=enclosure_file_path, help_text=_("Supported formats: M4A, MP3, MOV, MP4, M4V, PDF, and EPUB"))
    timedelta = models.DurationField(_("time delta"), null=True)
    type = models.CharField(_("type"), max_length=255, choices=TYPE_CHOICES, default="audio/mpeg")
    poster = models.ImageField(_("poster"), upload_to=enclosure_poster_path, blank=True, help_text=_("For video files"))
    cc = models.BooleanField(_("closed captions?"), default=False, help_text=_("For video files with closed captions"))

    class Meta:
        ordering = ["-episode__pub_date"]
        verbose_name = _("enclosure")
        verbose_name_plural = _("enclosures")

    def __str__(self):
        return "%s (%s)" % (self.episode, self.get_type_display())

    def save(self, *args, **kwargs):
        media = mutagen.File(self.file)
        try:
            length = media.info.length
        except AttributeError:
            length = 0
        self.timedelta = timedelta(seconds=int(length))
        super(Enclosure, self).save(*args, **kwargs)

    def get_poster_url(self):
        return self.poster.url if self.poster else self.episode.get_image_url()

    def get_cc(self):
        return "yes" if self.cc else "no"

    def get_megabytes(self):
        return "%.1f" % round(self.file.size / 1048576, 1)

    def get_duration(self):
        seconds = self.timedelta.total_seconds()
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        duration = "%02d:%02d" % (mins, secs)
        return "%02d:%s" % (hours, duration) if hours else duration
    get_duration.short_description = _("duration")

    def is_audio(self):
        return self.type in ["audio/mpeg", "audio/x-m4a"]

    def is_video(self):
        return self.type in ["video/mp4", "video/x-m4v", "video/quicktime"]

    def is_document(self):
        return self.type in ["application/pdf", "document/x-epub"]
