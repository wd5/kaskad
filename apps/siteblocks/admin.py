# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.siteblocks.models import Settings
from apps.utils.widgets import Redactor,RedactorMini
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin
from apps.siteblocks.models import News

class SettingsAdminForm(forms.ModelForm):
    class Meta:
        model = Settings

    def __init__(self, *args, **kwargs):
        super(SettingsAdminForm, self).__init__(*args, **kwargs)
        try:
            instance = kwargs['instance']
        except KeyError:
            instance = False
        if instance:
            if instance.type == u'input':
                self.fields['value'].widget = forms.TextInput()
            elif instance.type == u'textarea':
                self.fields['value'].widget = forms.Textarea()
            elif instance.type == u'redactor':
                self.fields['value'].widget = Redactor(attrs={'cols': 120, 'rows': 10},)

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title','value',)
    fields = ('title','value',)
    form = SettingsAdminForm

class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=RedactorMini(attrs={'cols': 170, 'rows': 30}),
        #label = u'анонс',
    )
    class Meta:
        model = News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('date_add', 'is_published',)
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    form = NewsAdminForm
    date_hierarchy = 'date_add'

admin.site.register(News, NewsAdmin)
admin.site.register(Settings, SettingsAdmin)