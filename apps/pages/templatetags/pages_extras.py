# -*- coding: utf-8 -*-
from apps.pages.models import Page
from apps.siteblocks.models import Settings
from django import template

register = template.Library()

@register.inclusion_tag("pages/block_page_summary.html")
def block_page_summary(alias):
    try:
        page = Page.objects.get(url = alias)
        return {'page': page}
    except Page.DoesNotExist:
        return {}

@register.inclusion_tag("pages/block_menu_by_pages.html")
def block_menu_by_pages(url,position):

    url = url.split('/')

    if url[1] and not url[2]:
        current = u'/%s/' % url[1]
    elif url[1] and url[2]:
        current = u'/%s/%s/' % (url[1],url[2])
    else:
        current = u'/'

    if url[1]:
        currentM = u'/%s/' % url[1]
    else:
        currentM = u'/'

    try:
        pages = Page.objects.filter(parent__isnull=True,is_published=True)
    except Page.DoesNotExist:
        pages = False

    try:
        pricepath = Settings.objects.get(name = 'pricelistpath').value
    except Settings.DoesNotExist:
        pricepath = False

    if pages:
        return {'pages': pages,'current':current,'currentM':currentM,'pricepath':pricepath,'position':position,}
    else:
        return {}

@register.inclusion_tag("pages/block_servicies.html")
def block_servicies():
    try:
        allpages = Page.objects.all()
        servicies = allpages.filter(parent = 1,is_published = True)
        basepath = allpages.get(id = 1).url
        return {'servicies': servicies, 'basepath':basepath, }
    except Page.DoesNotExist:
        return {'servicies':False,}

