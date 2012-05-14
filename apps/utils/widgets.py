# -*- coding: utf-8 -*-
from django import forms
import os
from django.utils.safestring import mark_safe


class Redactor(forms.Textarea):
    toolbar = u'default' #'mini'
    class Media:
        js = (
            '/static/js/jquery.js',
            '/static/js/redactor/redactor.js',
            )
        css = {
            'all': ('/static/js/redactor/css/redactor.css',)
        }

    def __init__(self, attrs=None):
        self.attrs = attrs
        if attrs:
            self.attrs.update(attrs)
        super(Redactor,self).__init__(attrs)

    def render(self,name,value,attrs=None):
        rendered = super(Redactor,self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
        $(document).ready(
            function()
            {
                $('#id_%s').redactor({ focus: true,toolbar: '%s', imageUpload: '/upload_img/', fileUpload: '/upload_file/' });
            }
        );
        </script>''' % (name,self.toolbar))


class RedactorMini(Redactor):
    toolbar = u'mini'

class RedactorMicro(Redactor):
    toolbar = u'micro'


class AdminImageWidget(forms.FileInput):
    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append((u'<a target="_blank" href="%s">'
                           u'<img src="%s" style="height: 100px;" /></a>'
                           u'<a href="/admin/crop/%s/?next=/admin/members/members/%s/">Изменить миниатюру</a>'
                           % (value.url, value.url, value.instance.id, value.instance.id)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))