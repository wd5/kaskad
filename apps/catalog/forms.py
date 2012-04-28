# -*- coding: utf-8 -*-
from django import forms
from apps.catalog.models import Review

class ReviewForm(forms.ModelForm):
    sender_name = forms.CharField(widget=forms.TextInput(attrs={'required':'required', 'placeholder':'Имя'}), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'required':'required', 'placeholder':'Текст отзыва','class':'faq_text'}), required=True)

    class Meta:
        model = Review
        fields = ('sender_name', 'text',)