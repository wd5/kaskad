# -*- coding: utf-8 -*-
#from django.template import loader, RequestContext, Context
#from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic.simple import direct_to_template


def index(request):
    template = 'index.html'

    return direct_to_template(
        request,
        template,
        {
            #'':
        }
    )