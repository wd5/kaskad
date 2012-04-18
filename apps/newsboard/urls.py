# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from apps.newsboard.views import LatestNewsFeed, LatestNewsSmiFeed
from apps.newsboard.models import NEWS_NORMAL, NEWS_SMI



urlpatterns = patterns('apps.newsboard.views',
    url(r'^/rss/$', LatestNewsFeed(), name='rss', ),
    url(r'^/$', 'news_list', name='index', ),
    url(r'^/view/(?P<pk>\d*)/$', 'news_detail', name='detail'),

)
