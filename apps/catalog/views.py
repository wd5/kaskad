# -*- coding: utf-8 -*-

from apps.catalog.models import Product,Category
from django.views.generic import ListView,DetailView,TemplateView


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

show_product = ShowProduct.as_view()

