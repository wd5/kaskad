# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

#from apps.app.urls import urlpatterns as app_url

urlpatterns = patterns('',

    #url(r'^/news/$', 'siteblocks.views.ShowNews'),
    url(r'^$', 'apps.views.index'),

)
#url(r'^captcha/', include('captcha.urls')),

#urlpatterns += #app_url


