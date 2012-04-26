# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.simple import direct_to_template
from apps.catalog.models import Category
from apps.siteblocks.models import News
from apps.pages.models import Page

class Index(TemplateView):
    template_name = 'pages/index.html'
    def get_context_data(self, **kwargs):
        context = super(Index,self).get_context_data()

        maincategory = Category.objects.published().filter(id__in=[1,2,3])
        catitems = Category.objects.published().exclude(id__in=[1,2,3])
        news = News.objects.published()
        context['maincategory'] = maincategory
        context['catitems'] = catitems
        context['news'] = news
        return context

index = Index.as_view()

def page(request, url):
    if not url.endswith('/'):
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    page = get_object_or_404(Page, url__exact=url)
    return direct_to_template(request, 'pages/default.html', locals())

@csrf_exempt
def static_page(request, template):
    return direct_to_template(request, template, locals())