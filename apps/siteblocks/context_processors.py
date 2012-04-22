# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings
from settings import SITE_NAME
import datetime

def settings(request):
    try:
        allsettings = Settings.objects.all()
    except Settings.DoesNotExist:
        allsettings = False

    if allsettings:
        try:
            address = allsettings.get(name='address').value
        except:
            address = ''
        try:
            phonenum = allsettings.get(name='phonenumber').value
        except:
            phonenum = ''
        try:
            phonecode = allsettings.get(name='phonecode').value
        except:
            phonecode = ''
        try:
            shuttertext = allsettings.get(name='shuttertext').value
        except:
            shuttertext = ''
        return {
                'phonenum':phonenum,
                'phonecode':phonecode,
                'shuttertext':shuttertext,
                'address': address,
                'site_name': SITE_NAME,
                'year':datetime.datetime.now(),
            }
    else:
        return {
                'phonenum':'',
                'phonecode':'',
                'shuttertext':'',
                'address': '',
                'site_name': SITE_NAME,
                'year':datetime.datetime.now(),
            }

