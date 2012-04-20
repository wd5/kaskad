# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
import datetime
import os
from pytils.translit import translify
from sorl.thumbnail import ImageField
from django.db.models.signals import post_save
from apps.utils.managers import PublishedManager
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

def image_path_Category(instance, filename):
    return os.path.join('images','categoty', translify(filename).replace(' ', '_') )

class Category(models.Model):
    title = models.CharField(verbose_name=u'название категории', max_length=150)
    description = models.TextField(verbose_name=u'описание')
    image = ImageField(upload_to=image_path_Category, verbose_name=u'картинка')
    slug = models.SlugField(verbose_name=u'Алиас', help_text=u'уникальное имя на латинице', unique=True)
    first_related_category = models.ForeignKey('self', verbose_name=u'дополнительная категория 1', related_name='first_additional', blank=True, null=True)
    second_related_category = models.ForeignKey('self', verbose_name=u'дополнительная категория 2', related_name='second_additional', blank=True, null=True)
    is_published = models.BooleanField(verbose_name=u'опубликовано', default=True)
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)

    objects = PublishedManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-order']
        verbose_name = _(u'category')
        verbose_name_plural = _(u'categories')

    def get_absolute_url(self):
        return u'/catalog/%s/' % self.slug

    def get_articles(self):
        return self.product_set.all()

    def get_first_additional(self):
            return self.first_related_category

    def get_second_additional(self):
            return self.second_related_category

def image_path_Product(instance, filename):
    return os.path.join('images','products', translify(filename).replace(' ', '_') )

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'категория')
    title = models.CharField(verbose_name=u'название товара', max_length=150)
    description = models.TextField(verbose_name=u'описание')
    price = models.DecimalField(verbose_name=u'цена', max_digits=10, decimal_places=2)
    image = ImageField(upload_to=image_path_Product, verbose_name=u'изображение')
    slug = models.SlugField(verbose_name=u'Алиас', help_text=u'уникальное имя на латинице', blank=True)
    is_published = models.BooleanField(verbose_name=u'опубликовано', default=True)
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)

    objects = PublishedManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-order']
        verbose_name = _(u'product')
        verbose_name_plural = _(u'products')

    def get_absolute_url(self):
        return u'%s%s/' % (self.category.get_absolute_url(),self.slug)

    def get_attached_photos(self):
        return self.attached_photo_set.all()

    def get_comments(self):
            return self.comment_set.all()

class Feature(models.Model):
    title = models.CharField(verbose_name=u'название характеристики', max_length=255)
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-order']
        verbose_name = _(u'feature')
        verbose_name_plural = _(u'features')

class FeatureValue(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'товар')
    feature = models.ForeignKey(Feature, verbose_name=u'характеристика')
    value = models.CharField(verbose_name=u'значение характеристики', max_length=150)

    def __unicode__(self):
        return u'%s' % ''

    class Meta:
        verbose_name = _(u'feature_value')
        verbose_name_plural = _(u'feature_values')

class Attached_photo(models.Model):
    product = models.ForeignKey(Product, verbose_name=u'товар')
    image = ImageField(upload_to=image_path_Product, verbose_name=u'изображение')
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', default=10)

    def __unicode__(self):
            return self.product.title

    class Meta:
        ordering = ['-order']
        verbose_name = _(u'attached_photo')
        verbose_name_plural = _(u'attached_photos')

class Comment(MPTTModel):
    product = models.ForeignKey(Product, verbose_name=u'товар')
    parent = TreeForeignKey('self', verbose_name=u'родительский комментарий', related_name='children', blank=True, null=True)
    order = models.IntegerField(u'порядок сортировки', help_text=u'Чем больше число, тем выше располагается элемент', blank=True)
    sender_name = models.CharField(verbose_name=u'имя отправителя', max_length=60)
    date_create = models.DateTimeField(u'дата комментария', default=datetime.datetime.now)
    text = models.TextField(verbose_name=u'текст комментария')
    is_moderated = models.BooleanField(verbose_name=u'публиковать комментарий', default=False)
    is_review = models.BooleanField(verbose_name=u'в отзывах', default=False)

    objects = TreeManager()

    class Meta:
        verbose_name =_(u'comment')
        verbose_name_plural =_(u'comments')
        ordering = ['-order']

    class MPTTMeta:
            order_insertion_by = ['order']

    def __unicode__(self):
        return u'%s - %s' % (self.sender_name,self.date_create)
