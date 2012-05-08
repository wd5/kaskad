# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView,DetailView,TemplateView
from apps.orders.models import Cart,CartProduct,Order
from apps.catalog.models import Product
from apps.orders.forms import RegistrationOrderForm
from pytils.numeral import choose_plural

class ViewCart(TemplateView):
    template_name = 'orders/cart_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ViewCart,self).get_context_data()

        sessionid = self.request.session.session_key

        try:
            cart = Cart.objects.get(sessionid=sessionid)
        except Cart.DoesNotExist:
            cart = False

        is_empty = True
        if cart:
            cart_products = cart.get_products()
        else:
            cart_products = False

        cart_str_total = u''
        if cart_products:
            is_empty = False
            cart_str_total = cart.get_str_total()

        context['is_empty'] = is_empty
        context['cart_products'] = cart_products
        context['cart_str_total'] = cart_str_total
        return context

view_cart = ViewCart.as_view()

@csrf_exempt
def add_product_to_cart(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'product_id' not in request.POST:
            return HttpResponseBadRequest()
        else:

            product_id = request.POST['product_id']
            try:
                product_id = int(product_id)
            except ValueError:
                return HttpResponseBadRequest()

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseBadRequest()

        cookies = request.COOKIES
        response = HttpResponse()

        cookies_cart_id = False
        if 'kaskad_cart_id' in cookies:
            cookies_cart_id = cookies['kaskad_cart_id']

        sessionid = request.session.session_key

        if cookies_cart_id:
            try:
                cart = Cart.objects.get(id=cookies_cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(sessionid=sessionid)
                response.set_cookie('kaskad_cart_id', cart.id, 1209600)
        else:
            try:
                cart = Cart.objects.get(sessionid=sessionid)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(sessionid=sessionid)

            response.set_cookie('kaskad_cart_id', cart.id, 1209600)

        try:
            cart_product = CartProduct.objects.get(
                cart=cart,
                product=product
            )
            cart_product.count += 1
            cart_product.save()
        except CartProduct.DoesNotExist:
            CartProduct.objects.create(
                cart=cart,
                product=product
            )
        is_empty = True
        cart_products_count = cart.get_products_count()
        cart_total = cart.get_str_total()
        cart_products_text = u''
        if cart_products_count:
            is_empty = False
            cart_products_text = u'товар%s' %(choose_plural(cart_products_count,(u'',u'а',u'ов')))

        cart_html = render_to_string(
            'orders/block_cart.html',
            {
                'is_empty':is_empty,
                'cart_products_count':cart_products_count,
                'cart_total':cart_total,
                'cart_products_text':cart_products_text
            }
        )
        response.content = cart_html
        return response

@csrf_exempt
def delete_product_from_cart(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'cart_product_id' not in request.POST:
            return HttpResponseBadRequest()
        else:

            cart_product_id = request.POST['cart_product_id']
            try:
                cart_product_id = int(cart_product_id)
            except ValueError:
                return HttpResponseBadRequest()

        try:
            cart_product = CartProduct.objects.get(id=cart_product_id)
        except CartProduct.DoesNotExist:
            return HttpResponseBadRequest()

        cart_product.delete()

        cookies = request.COOKIES
        response = HttpResponse()

        cookies_cart_id = False
        if 'kaskad_cart_id' in cookies:
            cookies_cart_id = cookies['kaskad_cart_id']

        sessionid = request.session.session_key

        if cookies_cart_id:
            try:
                cart = Cart.objects.get(id=cookies_cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(sessionid=sessionid)
                response.set_cookie('kaskad_cart_id', cart.id)
        else:
            try:
                cart = Cart.objects.get(sessionid=sessionid)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(sessionid=sessionid)

                response.set_cookie('kaskad_cart_id', cart.id)

        is_empty = True
        cart_products_count = cart.get_products_count()
        cart_total = u''
        cart_products_text = u''
        if cart_products_count:
            cart_total = cart.get_str_total()
            is_empty = False
            cart_products_text = u'товар%s' %(choose_plural(cart_products_count,(u'',u'а',u'ов')))
        '''
        cart_html = render_to_string(
            'orders/cart_block.html',
            {
                'is_empty':is_empty,
                'cart_products_count':cart_products_count,
                'cart_total':cart_total,
                'cart_products_text':cart_products_text
            }
        )
        cart_html = cart_html.replace(u'    ',u'').replace(u'\n',u'')
        '''
        #data = u'''{"cart_html":'%s',"cart_total":'%s'}'''%(cart_html,cart_total)
        data = u'''{"cart_total":'%s'}'''%cart_total
        response.content = data
        return response
