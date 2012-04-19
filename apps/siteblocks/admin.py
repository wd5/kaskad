# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.siteblocks.models import Settings
from apps.utils.widgets import Redactor,RedactorMini
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin
from apps.siteblocks.models import News

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title','name','value',)

class NewsAdminForm(forms.ModelForm):
    short_text = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 10}),
        #label = u'анонс',
    )
    text = forms.CharField(
        widget=Redactor(attrs={'cols': 170, 'rows': 30}),
        #label = u'анонс',
    )
    class Meta:
        model = News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('date_add', 'is_published',)
    list_filter = ('is_published',)
    form = NewsAdminForm
    date_hierarchy = 'date_add'

admin.site.register(News, NewsAdmin)
admin.site.register(Settings, SettingsAdmin)