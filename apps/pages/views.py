# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.simple import direct_to_template
from apps.catalog.models import Category
from apps.siteblocks.models import News
from apps.pages.models import Page

class Categories(ListView):
    model = Category
    context_object_name = 'category'
    template_name = 'pages/index.html'

def index(request):
    try:
        maincategory = Category.objects.filter(id__in=[1,2,3])
    except Category.DoesNotExist:
        maincategory = False
    try:
        catitems = Category.objects.exclude(id__in=[1,2,3])
    except Category.DoesNotExist:
        catitems = False
    try:
        news = News.objects.all()
    except News.DoesNotExist:
        news = False
    return direct_to_template(request, 'pages/index.html', locals())

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