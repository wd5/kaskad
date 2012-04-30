# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^faq/$','apps.faq.views.questions_list'),

    url(r'^news/$', 'apps.siteblocks.views.news_list'),

    url(r'^reviews/$', 'apps.catalog.views.reviews_list'),

    url(r'^$', 'apps.pages.views.index'),

    url(r'^catalog/$', 'apps.pages.views.index'),
    url(r'^catalog/(?P<slug>[^/]+)/$', 'apps.catalog.views.show_category'),
    url(r'^catalog/[^/]+/(?P<slug>[^/]+)/$', 'apps.catalog.views.show_product'),

    url(r'^do_comment/$', 'apps.catalog.views.do_comment'),

    url(r'^services/$', 'apps.pages.views.show_services'),
    url(r'^services/(?P<slug>[^/]+)/$', 'apps.pages.views.show_service'),

    url(r'^articles/$', 'apps.pages.views.show_articles'),
    url(r'^articles/(?P<slug>[^/]+)/$', 'apps.pages.views.show_article'),

)
#url(r'^captcha/', include('captcha.urls')),



