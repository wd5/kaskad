# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.faq.models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','question','pub_date','published',)
    list_display_links = ('id','question','pub_date',)
    list_editable = ('published',)
    search_fields = ('question', 'answer',)
    list_filter = ('pub_date','published',)
    fields = ('pub_date','name','email','question','answer','author','published',)

admin.site.register(Question, QuestionAdmin)