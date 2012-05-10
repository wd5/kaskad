# -*- coding: utf-8 -*-
from apps.siteblocks.models import Settings
from settings import SITE_NAME

def settings(request):
    try:
        allsettings = Settings.objects.all()
    except Settings.DoesNotExist:
        allsettings = False

    if allsettings:
        try:
            contacts = allsettings.get(name='contacts').value
        except:
            contacts = ''
        try:
            shuttertext = allsettings.get(name='shuttertext').value
        except:
            shuttertext = ''
        return {
                'contacts':contacts,
                'shuttertext':shuttertext,
                'site_name': SITE_NAME,
            }
    else:
        return {
                'contacts':'',
                'shuttertext':'',
                'site_name': SITE_NAME,
            }

