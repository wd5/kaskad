# -*- coding: utf-8 -*-
from django.core.serializers import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from apps.catalog.models import Product, Category, Review, Comment
from django.views.generic import DetailView, FormView, CreateView, ListView
from apps.catalog.forms import CommentForm
from apps.utils.views import CreateViewMixin
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest

class ShowCategory(DetailView):
    model = Category
    template_name = 'catalog/show_category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = kwargs
        context_object_name = self.get_context_object_name(self.object)

        context['products'] = self.object.get_products()

        if context_object_name:
            context[context_object_name] = self.object
        return context

show_category = ShowCategory.as_view()

class ShowProduct(DetailView):
    model = Product
    template_name = 'catalog/show_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = kwargs
        context_object_name = self.get_context_object_name(self.object)

        context['comments'] = self.object.get_comments()

        if context_object_name:
            context[context_object_name] = self.object
        return context

show_product = ShowProduct.as_view()

class ShowReviews(ListView):
    model = Review
    template_name = 'catalog/show_reviews.html'
    context_object_name = 'reviews'
    queryset = model.objects.published()

reviews_list = ShowReviews.as_view()

class CommentFormProduct(FormView):
    form_class = CommentForm
    template_name = 'catalog/comment_form.html'

    def get_form_kwargs(self):
        kwargs = super(CommentFormProduct, self).get_form_kwargs()
        initial = self.get_initial()

        slug = self.kwargs['slug']
        try:
            node = self.kwargs['node']
        except KeyError:
            node = None

        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return HttpResponseBadRequest()

        initial['product'] = product
        if node:
            try:
                parent = Comment.objects.get(id=node)
            except Comment.DoesNotExist:
                return HttpResponseBadRequest()
        initial['parent'] = node

        kwargs.update({
            'initial': initial,

        })
        return kwargs

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form

        slug = self.kwargs['slug']
        try:
            product = Product.objects.filter(slug=slug)
            context['form'].fields['product'].queryset = product
        except Product.DoesNotExist:
            return HttpResponseBadRequest()

        try:
            node = self.kwargs['node']
        except KeyError:
            node = False

        if node:
            try:
                parent = Comment.objects.filter(id=node)
                context['form'].fields['parent'].queryset = parent
            except Comment.DoesNotExist:
                return HttpResponseBadRequest()
        else:
            context['form'].fields['parent'].queryset = Comment.objects.extra(where=['1=0'])

        return self.render_to_response(context)

show_comment_form = CommentFormProduct.as_view()

@csrf_exempt
def do_comment(request):
    if request.is_ajax():
        data = request.POST.copy()

        try:
            product_id = data['product']
        except KeyError:
            return HttpResponseBadRequest()

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseBadRequest()

        data['product'] = product.id

        comment_form = CommentForm(data)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponse('success')
        else:
            product_set = Product.objects.filter(pk=product_id)
            comment_form.fields['product'].queryset = product_set


            id_parent = data['parent']
            try:
                id_parent = int(id_parent)
            except:
                id_parent = False

            if id_parent:
                try:
                    parent = Comment.objects.filter(id=id_parent)
                    comment_form.fields['parent'].queryset = parent
                except Comment.DoesNotExist:
                    return HttpResponseBadRequest()
            else:
                comment_form.fields['parent'].queryset = Comment.objects.extra(where=['1=0'])

            comment_form_html = render_to_string(
                'catalog/comment_form.html',
                    {'form': comment_form}
            )
            return HttpResponse(comment_form_html)
    else:
        return HttpResponseBadRequest()