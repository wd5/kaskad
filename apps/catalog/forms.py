# -*- coding: utf-8 -*-
from django import forms
from apps.catalog.models import Review,Comment

class ReviewForm(forms.ModelForm):
    sender_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя'}), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Текст отзыва','class':'faq_text'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'E-mail'}), required=True)

    class Meta:
        model = Review
        fields = ('sender_name', 'text', 'email',)

class CommentForm(forms.ModelForm):
    sender_name = forms.CharField(widget=forms.TextInput(attrs={}), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'faq_text'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={}), required=True)

    class Meta:
        model = Comment
        fields = ('sender_name', 'text', 'email',)