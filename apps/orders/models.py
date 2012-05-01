# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
import datetime
import os

class Cart(models.Model):
    create_date = models.DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.now)
