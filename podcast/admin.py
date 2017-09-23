from __future__ import unicode_literals

from django.contrib import admin

from .models import Speaker, Category, Show, Episode, Enclosure


class EnclosureInline(admin.TabularInline):
    model = Enclosure
    fields = ('file', 'type', 'poster', 'cc', 'get_duration',)
    readonly_fields = ('get_duration',)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)


class CateogryAdmin(admin.ModelAdmin):
    list_display = ('full', 'parent',)
    prepopulated_fields = {'slug': ('title',)}


class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_latest_duration', 'get_latest_pub_date',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories', 'hosts',)
    fieldsets = (
        (None, {
            'fields': ('type', 'title', 'slug', 'image', 'description',)
        }),
        ('iTunes', {
            'fields': ('subtitle', 'summary', 'author_name', 'author_email', 'owner_name', 'owner_email', 'copyright', 'categories', 'explicit', 'block', 'complete', 'itunes',),
        }),
        ('Speakers', {
            'fields': ('hosts',),
        }),
    )


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_duration', 'pub_date', 'show', 'explicit',)
    list_filter = ('show',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('show', 'title', 'slug', 'description', 'pub_date',)
        }),
        ('iTunes', {
            'fields': ('type', 'season', 'number', 'itunes_title', 'summary', 'notes', 'author_name', 'author_email', 'image', 'explicit', 'block',),
        }),
        ('Speakers', {
            'fields': ('hosts', 'guests',),
        }),
    )
    inlines = [
        EnclosureInline,
    ]


class EnclosureAdmin(admin.ModelAdmin):
    list_display = ('episode', 'get_duration', 'type', 'file',)
    fields = ('episode', 'type', 'file', 'poster', 'cc', 'get_duration',)
    readonly_fields = ('get_duration',)


admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Category, CateogryAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Enclosure, EnclosureAdmin)
