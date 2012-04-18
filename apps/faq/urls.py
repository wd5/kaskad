# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from apps.faq.views import questions_list, send_question


urlpatterns = patterns('',
    (r'^faq/$',questions_list),

    (r'^send_question/$',send_question),




)