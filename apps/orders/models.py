# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from apps.catalog.models import Product
import datetime
import os

class Cart(models.Model):
    create_date = models.DateTimeField(verbose_name=u'Дата создания', default=datetime.datetime.now)
    sessionid = models.CharField(max_length=50, verbose_name=u'ID сессии')

    class Meta:
        verbose_name = _(u'cart')
        verbose_name_plural = _(u'carts')

    def __unicode__(self):
        return u'%s - %s' % (self.sessionid,self.create_date)

    def get_products(self):
        return CartProduct.objects.select_related().filter(cart=self)

    def get_products_count(self):
        return self.get_products().count()

    def get_total(self):
        sum = 0
        for cart_product in self.cartproduct_set.select_related().all():
            sum += cart_product.get_total()
        return sum

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

    def __unicode__(self):
        return u'на %s руб.' % self.get_str_total()

from django.db.models.signals import post_save
def delete_old_carts(sender, instance, created, **kwargs):
    if created:
        now = datetime.datetime.now()
        day_ago30 = now - datetime.timedelta(days=30)
        carts = Cart.objects.filter(create_date__lte=day_ago30)
        if carts:
            carts.delete()

post_save.connect(delete_old_carts, sender=CartProduct)

class Order(models.Model):
    fullname = models.CharField(max_length=150, verbose_name=u'Фамилия Имя Отчество')
    create_date = models.DateTimeField(verbose_name=u'Дата оформления', default=datetime.datetime.now)
    contact_info = models.CharField(max_length=255, verbose_name=u'Контактная информация')

    class Meta:
        verbose_name = _(u'order_item')
        verbose_name_plural = _(u'order_items')
        ordering = ('-create_date',)

    def __unicode__(self):
        return u'%s - %s' % (self.fullname,self.create_date)

    def get_products(self):
        return self.orderproduct_set.select_related().all()

    def get_products_count(self):
        return self.get_products().count()

    def get_total(self):
        sum = 0
        for order_product in self.orderproduct_set.select_related().all():
            sum += order_product.get_total()
        return sum

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

    def admin_summary(self):
        return '<span>%s</span>' % self.get_str_total()
    admin_summary.allow_tags = True
    admin_summary.short_description = 'Сумма'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'Заказ')
    count = models.PositiveIntegerField(default=1, verbose_name=u'Количество')
    product = models.ForeignKey(Product, verbose_name=u'Товар')

    def __unicode__(self):
        return u'на сумму %s руб.' % self.get_str_total()

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

