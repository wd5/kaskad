# -*- coding: utf-8 -*-
from apps.catalog.models import Product
from apps.orders.models import Cart, OrderProduct
from django.db.models import Max, Count, Sum
from django import template
from pytils.numeral import choose_plural

register = template.Library()

@register.inclusion_tag("orders/block_cart.html", takes_context=True)
def block_cart(context):
    if 'request' in context:
        request = context['request']

        cookies = request.COOKIES

        cookies_cart_id = False
        if 'kaskad_cart_id' in cookies:
            cookies_cart_id = cookies['kaskad_cart_id']

        sessionid = request.session.session_key

        if cookies_cart_id:
            try:
                cart = Cart.objects.get(id=cookies_cart_id)
            except Cart.DoesNotExist:
                cart = False
        else:
            try:
                cart = Cart.objects.get(sessionid=sessionid)
            except Cart.DoesNotExist:
                cart = False
    else:
        cart = False

    try:
        popular_products = OrderProduct.objects.values('product').annotate(pcount=Sum('count')).order_by('-pcount')[:1]
    except OrderProduct.DoesNotExist:
        popular_products = False

    popular_product = False

    if popular_products:
        try:
            popular_product = Product.objects.get(id=popular_products[0]['product'])
        except Product.DoesNotExist:
            popular_product = False

    is_empty = True
    cart_total = 0
    cart_products_count = 0
    cart_products_text = u''
    if cart:
        cart_products_count = cart.get_products_count()
        if cart_products_count:
            cart_total = cart.get_str_total()
            is_empty = False
            cart_products_text = u'товар%s' % (choose_plural(cart_products_count, (u'', u'а', u'ов')))
    return {
        'is_empty': is_empty,
        'cart_products_count': cart_products_count,
        'cart_total': cart_total,
        'cart_products_text': cart_products_text,
        'popular_product':popular_product
    }


@register.simple_tag()
def get_sum(cl):
    rl = cl.result_list
    sum = 0
    for order in rl:
        sum += order.get_total_summary()
    return sum