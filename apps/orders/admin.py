# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.orders.models import Cart,CartProduct,Order

class CartProductInlines(admin.TabularInline):
    model = CartProduct
    readonly_fields = ('product',)
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('id','create_date','sessionid',)
    list_display_links = ('id','create_date','sessionid',)
    list_filter = ('create_date',)
    inlines = [CartProductInlines]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','fullname','contact_info','cart',)
    list_display_links = ('id','fullname','contact_info','cart',)
    search_fields = ('fullname','contact_info',)

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
