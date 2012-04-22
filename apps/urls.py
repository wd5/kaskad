# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    #url(r'^/news/$', 'siteblocks.views.ShowNews'),
    url(r'^$', 'apps.pages.views.index'),
    url(r'^catalog/$', 'apps.pages.views.index'),
    url(r'^catalog/(?P<catalog_slug>[^/]+)/$', 'apps.pages.views.index'),

)
#url(r'^captcha/', include('captcha.urls')),



