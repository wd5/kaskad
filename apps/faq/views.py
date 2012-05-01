# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import redirect
from django.views.generic import CreateView
from apps.faq.forms import QuestionForm
from apps.faq.models import Question
from apps.utils.views import CreateViewMixin

class SendQuestion(CreateViewMixin,CreateView):
    form_class = QuestionForm
    template_name = 'faq/questions.html'
    context_object_name = 'form'
    success_url = '/faq/thanks/'

    def form_valid(self, form):
        Question.objects.create(**form.cleaned_data)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SendQuestion, self).get_context_data(**kwargs)
        if self.kwargs.get('action',None)=='thanks':
            context['is_successed'] = True
        else:
            context['is_successed'] = False
        context['questions'] = Question.objects.filter(published=True)
        return context

questions_list = SendQuestion.as_view()