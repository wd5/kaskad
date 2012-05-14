# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^faq/$','apps.faq.views.questions_list'),
    url(r'^faq/(?P<action>[^/]+)/$','apps.faq.views.questions_list'),

    url(r'^news/$', 'apps.siteblocks.views.news_list'),

    url(r'^reviews/$', 'apps.catalog.views.reviews_list'),
    url(r'^reviews/(?P<action>[^/]+)/$', 'apps.catalog.views.reviews_list'),

    url(r'^$', 'apps.pages.views.index'),

    url(r'^catalog/(?P<slug>[^/]+)/$', 'apps.catalog.views.show_category'),
    url(r'^catalog/[^/]+/(?P<slug>[^/]+)/comment/$', 'apps.catalog.views.show_comment_form'),
    url(r'^catalog/[^/]+/(?P<slug>[^/]+)/comment/(?P<node>[^/]+)/$', 'apps.catalog.views.show_comment_form'),
    url(r'^catalog/[^/]+/(?P<slug>[^/]+)/$', 'apps.catalog.views.show_product'),

    url(r'^services/$', 'apps.pages.views.show_services'),
    url(r'^services/(?P<slug>[^/]+)/$', 'apps.pages.views.show_service'),

    url(r'^articles/$', 'apps.pages.views.show_articles'),
    url(r'^articles/(?P<slug>[^/]+)/$', 'apps.pages.views.show_article'),

    url(r'^do_comment/$','apps.catalog.views.do_comment'),

    url(r'^cart/$','apps.orders.views.view_cart'),
    url(r'^add_product_to_cart/$','apps.orders.views.add_product_to_cart'),
    url(r'^delete_product_from_cart/$','apps.orders.views.delete_product_from_cart'),
    url(r'^change_cart_product_count/$','apps.orders.views.change_cart_product_count'),
    url(r'^show_order_form/$','apps.orders.views.show_order_form'),
    url(r'^registration_order/$','apps.orders.views.registration_order')

)
#url(r'^captcha/', include('captcha.urls')),



