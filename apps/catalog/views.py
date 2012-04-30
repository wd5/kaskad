# -*- coding: utf-8 -*-

from apps.catalog.models import Product,Category,Review
from django.views.generic import DetailView,ListView,CreateView
from apps.catalog.forms import ReviewForm,CommentForm
from django.shortcuts import redirect

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

class ShowReviews(CreateView):
    form_class = ReviewForm
    template_name = 'catalog/show_reviews.html'
    context_object_name = 'form'
    succes_url = '/reviews/'

    def form_valid(self, form):
        Review.objects.create(**form.cleaned_data)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ShowReviews, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(is_moderated=True)
        return context

reviews_list = ShowReviews.as_view()

class DoComment(CreateView):
    form_class = CommentForm
    template_name = 'catalog/do_comment.html'
    context_object_name = 'form'

    def form_valid(self, form):
        Review.objects.create(**form.cleaned_data)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.path

do_comment = DoComment.as_view()