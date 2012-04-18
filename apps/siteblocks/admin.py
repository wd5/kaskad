# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.siteblocks.models import SiteMenu, Settings
from apps.utils.widgets import RedactorMini
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin


class SiteMenuAdmin(AdminImageMixin, MPTTModelAdmin):
    list_display = ('title', 'url', 'order', 'is_published',)
    list_display_links = ('title', 'url',)
    list_editable = ('order', 'is_published',)

admin.site.register(SiteMenu, SiteMenuAdmin)

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title','name','value',)

admin.site.register(Settings, SettingsAdmin)
