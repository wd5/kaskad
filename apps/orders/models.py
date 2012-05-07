# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from apps.catalog.models import Product
import datetime
import os

class Cart(models.Model):
    fullname = models.CharField(max_length=150, verbose_name=u'Фамилия Имя Отчество')
    contact_info = models.CharField(max_length=255, verbose_name=u'Контактная информация')
    create_date = models.DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.now)
    sessionid = models.CharField(max_length=50, verbose_name=u'ID сессии')
    is_issued = models.BooleanField(verbose_name=u'Заказ оформлен', default=True)
    #products = models.ManyToManyField(Product, through="CartProduct", blank=True, verbose_name=u'Товары', related_name='cart_products')

    class Meta:
        verbose_name = _(u'cart')
        verbose_name_plural = _(u'carts')

    def __unicode__(self):
        return self.sessionid

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=u'Корзина')
    count = models.PositiveIntegerField(default=1, verbose_name=u'Количество')
    product = models.ForeignKey(Product, verbose_name=u'Товар')

    class Meta:
        verbose_name =_(u'product_item')
        verbose_name_plural =_(u'product_items')

    def get_total(self):
        total = self.product.price * self.count
        return total

    def get_str_total(self):
        total = self.get_total()
        value = u'%s' %total
        if total._isinteger():
            value = u'%s' %value[:len(value)-3]
            count = 3
        else:
            count = 6

        if len(value)>count:
            ends = value[len(value)-count:]
            starts = value[:len(value)-count]

            return u'%s %s' %(starts, ends)
        else:
            return value