# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from django.views.generic import ListView, CreateView, DetailView
from django.shortcuts import get_object_or_404
from django import http
from apps.siteblocks.models import News

class NewsListView(ListView):
    template_name = 'pages/news.html'
    model = News
    context_object_name = 'news'

    def get_queryset(self):
        qs = News.objects.published()
        return qs

news_list = NewsListView.as_view()

