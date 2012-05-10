# -*- coding: utf-8 -*-
import datetime
from django.core.mail.message import EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView,DetailView,TemplateView
from apps.orders.models import Cart,CartProduct,Order, OrderProduct
from apps.catalog.models import Product
from apps.siteblocks.models import Settings
from apps.orders.forms import RegistrationOrderForm
from pytils.numeral import choose_plural
import settings

class ViewCart(TemplateView):
    template_name = 'orders/cart_detail.html'
    def get_context_data(self, **kwargs):
        context = super(ViewCart,self).get_context_data()

        sessionid = self.request.session.session_key

        try:
            cart = Cart.objects.get(sessionid=sessionid)
            cart_id = cart.id
        except Cart.DoesNotExist:
            cart = False
            cart_id = False

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
        context['cart_id'] = cart_id
        return context

view_cart = ViewCart.as_view()

@csrf_exempt
def show_order_form(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'cart_id' not in request.POST:
            return HttpResponseBadRequest()
        else:
            cart_id = request.POST['cart_id']
            try:
                cart_id = int(cart_id)
            except ValueError:
                return HttpResponseBadRequest()

        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = False

        if cart:
            cart_products = cart.get_products()
        else:
            cart_products = False

        cart_str_total = u''
        if cart_products:
            cart_str_total = cart.get_str_total()

        response = HttpResponse()
        order_form = RegistrationOrderForm()

        order_html = render_to_string(
            'orders/order_form.html',
                {
                'cart_products':cart_products,
                'cart_str_total':cart_str_total,
                'form':order_form
            }
        )
        response.content = order_html
        return response

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
        data = u'''{"cart_total":'%s'}'''%cart_total
        response.content = data
        return response

@csrf_exempt
def change_cart_product_count(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        if 'cart_product_id' not in request.POST or 'new_count' not in request.POST:
            return HttpResponseBadRequest()

        cart_product_id = request.POST['cart_product_id']
        try:
            cart_product_id = int(cart_product_id)
        except ValueError:
            return HttpResponseBadRequest()

        new_count = request.POST['new_count']
        try:
            new_count = int(new_count)
        except ValueError:
            return HttpResponseBadRequest()

        try:
            cart_product = CartProduct.objects.get(id=cart_product_id)
        except CartProduct.DoesNotExist:
            return HttpResponseBadRequest()

        cart_product.count = new_count
        cart_product.save()
        cart_str_total = cart_product.cart.get_str_total()

        data = u'''{"tr_str_total":'%s', "cart_str_total":'%s'}'''%(cart_product.get_total(),cart_str_total)

        return HttpResponse(data)

@csrf_exempt
def registration_order(request):
    if not request.is_ajax():
        return HttpResponseRedirect('/')
    else:
        cookies = request.COOKIES

        cookies_cart_id = False
        if 'kaskad_cart_id' in cookies:
            cookies_cart_id = cookies['kaskad_cart_id']

        sessionid = request.session.session_key
        response = HttpResponse()
        badresponse = HttpResponseBadRequest()

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

        if not cart:
            return HttpResponseBadRequest()

        cart_products = cart.get_products()
        cart_products_count = cart_products.count()

        if not cart_products_count:
            return HttpResponseBadRequest()

        registration_order_form = RegistrationOrderForm(data=request.POST)

        if registration_order_form.is_valid():
            cd = registration_order_form.cleaned_data
            #добавили заказ
            new_order = registration_order_form.save()

            for cart_product in cart_products:
                OrderProduct.objects.create(
                    order=new_order,
                    count=cart_product.count,
                    product=cart_product.product
                )

            cart.delete() #Очистка и удаление корзины
            response.delete_cookie('kaskad_cart_id')

            subject = u'ООО Каскад - Информация по заказу.'
            subject = u''.join(subject.splitlines())
            message = render_to_string(
                'orders/message_template.html',
                {
                    'order':new_order,
                    'products':new_order.get_products()
                }
            )

            try:
                emailto = Settings.objects.get(name='workemail').value
            except Settings.DoesNotExist:
                emailto = False

            if emailto:
                msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,[emailto])
                msg.content_subtype = "html"
                msg.send()
            messageToUser = 'Спасибо за заказ. Номер вашего заказа №<i>%s</i>. В ближайшее время с вами свяжется наш менеджер.' % new_order.id
            response.content = messageToUser
            return response
        else:
            cart_str_total = cart.get_str_total()
            order_html = render_to_string(
                'orders/order_form.html',
                    {
                    'cart_products':cart_products,
                    'cart_str_total':cart_str_total,
                    'form':registration_order_form
                }
            )
            badresponse.content = order_html
            return badresponse