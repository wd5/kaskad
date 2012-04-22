# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings
from django import template
from django.conf import settings
import os.path, time, datetime

register = template.Library()

@register.inclusion_tag("siteblocks/block_setting.html")
def block_static(name):
    try:
        setting = Settings.objects.get(name = name)
    except Settings.DoesNotExist:
        setting = False
    return {'block': block,}

@register.inclusion_tag("siteblocks/block_price.html")
def block_price():
    try:
        pricepath = Settings.objects.get(name = 'pricelistpath').value
    except Settings.DoesNotExist:
        pricepath = False
    if pricepath:
        path = settings.MEDIA_ROOT + pricepath
        try:
            priceupdate = datetime.date.fromtimestamp(os.path.getmtime(path))
        except OSError:
            priceupdate = False
    return {'pricepath': pricepath,'priceupdate': priceupdate,}
