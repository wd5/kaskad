# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


from django.template.loader import render_to_string
from django.core.mail import send_mail

from pytils.translit import slugify
from djangosphinx.models import SphinxSearch

from apps.utils.managers import PublishedManager

class NewsCategory(models.Model):
    title = models.CharField(
        verbose_name = u'название',
        max_length = 50,
    )
    order = models.PositiveIntegerField(
        verbose_name = u'сортировка',
        default = 0
    )
    class Meta:
        ordering = ['order',]
        verbose_name = u'категория новости'
        verbose_name_plural = u'категории новостей'
    def __unicode__(self):
        return u'%s' % self.title

class News(models.Model):
    title = models.CharField(
        verbose_name = u'заголовок',
        max_length = 250,
    )
    category = models.ForeignKey(
        NewsCategory,
        verbose_name = u'категория новости',
        null = True,
        blank = True,
    )
    image = models.ImageField(
        verbose_name = 'изображение',
        upload_to = u'images/news/',
        blank = True,
        null = True,
    )
    short_text = models.TextField(
        verbose_name = u'анонс',
        blank = True,
        null = True,
    )
    text = models.TextField(
        verbose_name = u'текст',
    )
    on_main_page = models.BooleanField(
        verbose_name = u'показывать на главной',
        default = True,
    )
    is_published = models.BooleanField(
        verbose_name = u'опубликовано',
        default = True,
    )
    date_add = models.DateTimeField(
        verbose_name = u'дата создания',
        default = datetime.now
    )
    # Managers
    objects = PublishedManager()

    class Meta:
        ordering = ['-date_add', '-id',]
        verbose_name =_(u'news_item')
        verbose_name_plural =_(u'news_items')
        get_latest_by = 'date_add'

    def __unicode__(self):
        return self.title