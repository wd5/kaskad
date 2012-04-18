# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.faq.models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','published',)
    list_display_links = ('id','pub_date',)
    search_fields = ('question', 'answer',)
    list_filter = ('pub_date','published',)

admin.site.register(Question, QuestionAdmin)