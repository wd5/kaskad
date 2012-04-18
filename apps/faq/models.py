# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _

class Question(models.Model):
    pub_date = models.DateTimeField(verbose_name = u'Дата', default=datetime.datetime.now)
    name = models.CharField(max_length = 150, verbose_name = u'Имя')
    email = models.CharField(verbose_name=u'E-mail',max_length=75)
    question = models.TextField(verbose_name = u'Вопрос')
    answer = models.TextField(verbose_name = u'Ответ', blank = True)
    author = models.CharField(max_length = 150, verbose_name = u'Автор ответа', help_text=u'Например: менеджер',blank=True)
    published = models.BooleanField(verbose_name = u'Опубликовано', default=False)

    class Meta:
        verbose_name = _(u'question')
        verbose_name_plural = _(u'questions')
        ordering = ['-pub_date']

    def __unicode__(self):
        return u'Вопрос от %s' % self.pub_date