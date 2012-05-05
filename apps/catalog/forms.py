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
    class Meta:
        model = Comment
        exclude = ('date_create', 'is_moderated',)

class CommentFormValid(CommentForm):
    #product = forms.CharField(required=True)
    #parent = forms.CharField(required=False)
    sender_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя'}), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Текст комментария','class':'faq_text'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'E-mail'}), required=True)

    class Meta:
        model = Comment
        exclude = ('date_create', 'is_moderated',)