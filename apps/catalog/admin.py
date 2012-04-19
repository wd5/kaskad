# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from apps.utils.widgets import Redactor,RedactorMini
from sorl.thumbnail.admin import AdminImageMixin
from mptt.admin import MPTTModelAdmin
from apps.catalog.models import Category,Product,Attached_photo,Comment

class CategoryAdmin(AdminImageMixin,admin.ModelAdmin):
    list_display = ('id','title','slug','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('order','is_published','slug',)
    list_filter = ('is_published',)
    search_fields = ('title',)
    raw_id_fields = ('first_related_category','second_related_category',)

class AttachedPhotoInline(AdminImageMixin,admin.TabularInline):
    model = Attached_photo

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=RedactorMini(attrs={'cols': 100, 'rows': 7}))
    description.label=u'описание'
    #!
    features_table = forms.CharField(widget=RedactorMini(attrs={'cols': 100, 'rows': 7}))
    features_table.label=u'технические характеристики'

    class Meta:
        model = Product

class ProductAdmin(AdminImageMixin,admin.ModelAdmin):
    list_display = ('id','title','category','price','slug','order','is_published',)
    list_display_links = ('id','title',)
    list_editable = ('price','slug','order','is_published',)
    list_filter = ('is_published','price','category',)
    search_fields = ('title','description','price','category__title',)
    raw_id_fields = ('category',)
    inlines = [AttachedPhotoInline,]
    form = ProductAdminForm

class CommentAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=RedactorMini(attrs={'cols': 170, 'rows': 20}),
        label = u'Текст комментария',
    )
    def __init__(self, *args, **kwargs):
        super(CommentAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Comment.objects\
            .exclude(id__exact=self.instance.pk)
    class Meta:
        model = Comment

class CommentAdmin(MPTTModelAdmin):
    list_display = ('id','sender_name','date_create','is_moderated','is_review',)
    list_display_links = ('id','sender_name','date_create',)
    list_editable = ('is_moderated','is_review',)
    list_filter = ('is_moderated','is_review','sender_name','date_create',)
    search_fields = ('product__title','text','sender_name',)
    list_select_related = True

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)