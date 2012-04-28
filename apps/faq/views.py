# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import redirect
from django.views.generic import FormView,ListView,CreateView
from apps.faq.forms import QuestionForm
from apps.faq.models import Question

class SendQuestion(CreateView):
    form_class = QuestionForm
    template_name = 'faq/questions.html'
    context_object_name = 'form'
    succes_url = '/faq/'

    def form_valid(self, form):
        Question.objects.create(**form.cleaned_data)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SendQuestion, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(published=True)
        return context

questions_list = SendQuestion.as_view()