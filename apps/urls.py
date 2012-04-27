# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^news/$', 'apps.siteblocks.views.news_list'),
    url(r'^$', 'apps.pages.views.index'),
    url(r'^catalog/$', 'apps.pages.views.index'),
    url(r'^catalog/(?P<slug>[^/]+)/$', 'apps.catalog.views.show_category'),
    url(r'^catalog/[^/]+/(?P<slug>[^/]+)/$', 'apps.catalog.views.show_product'),
    url(r'^services/(?P<slug>[^/]+)/$', 'apps.pages.views.show_service'),

)
#url(r'^captcha/', include('captcha.urls')),



