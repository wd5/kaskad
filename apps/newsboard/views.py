# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from django.views.generic import ListView, CreateView, DetailView
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django import http
from apps.newsboard.models import News, NewsCategory

class NewsListView(ListView):
    model = News
    paginate_by = 6

    def get_categories_list(self, **kwargs):
        return NewsCategory.objects.all()

    def get_queryset(self):
        from django.db.models import Q
        query = self.queryset.published()

        date = self.request.GET.get('date', None)
        if date:
            date = date.split('.')
            query = query.filter(
                Q(date_add__year = date[2]) & /
                Q(date_add__month = date[1]) & /
                Q(date_add__day = date[0])
            )
        return query

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['categories_list'] = self.categories_list()
        context['current_date'] = self.request.GET.get('date', None)
        return context

news_list = NewsListView.as_view()


class NewsDetailView(DetailView):
    context_object_name = 'news_current'
    model = News

    def get_template_names(self, **kwargs):
        return ['newsboard/detail.html']

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['categories_list'] = NewsListView.get_categories_list()
        return context

news_detail = NewsDetailView.as_view()

class LatestNewsFeed(Feed):
    title = _(u'Новости')
    link = '/news/'
    description = ''

    def items(self):
        return News.objects.published()[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_text