# -*- coding: utf-8 -*-
DATABASE_NAME = u'kaskad'
PROJECT_NAME = u'kaskad'
SITE_NAME = u'КАСКАД'
DEFAULT_FROM_EMAIL = u'support@kaskad.octweb.ru'

from config.base import *

try:
    from config.development import *
except ImportError:
    from config.production import *

TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'apps.siteblocks',
    'apps.pages',
    'apps.faq',
    'apps.catalog',
    'apps.orders',

    'sorl.thumbnail',
    #'south',
    #'captcha',
)

MIDDLEWARE_CLASSES += (
    'apps.pages.middleware.PageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'apps.pages.context_processors.meta',
    'apps.siteblocks.context_processors.settings',
)