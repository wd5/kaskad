from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.conf import settings

from apps.urls import urlpatterns as apps_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    (r'^admin/upload_pricelist/$', 'views.upload_pricelist'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

     #Redactor
    (r'^upload_img/$', 'views.upload_img'),
    (r'^upload_file/$', 'views.upload_file'),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

)

urlpatterns += apps_urlpatterns

urlpatterns += patterns('apps.pages.views',
(r'^(?P<url>.*)$', 'page'),
)