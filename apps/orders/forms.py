# -*- coding: utf-8 -*-
from django import forms
from apps.orders.models import Order

class RegistrationOrderForm(forms.ModelForm):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Контактное лицо'}), required=True)
    contact_info = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'E-mail, номер телефона'}), required=True)


    class Meta:
        model = Order
        exclude = ('create_date',)