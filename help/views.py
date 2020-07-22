import json
import urllib

from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django_hosts.resolvers import reverse
import requests

from .forms import ContactForm
from .models import News
from .models import UsageExamples



class Top(FormView):
    """Top Page"""
    template_name='help/top.html'
    form_class = ContactForm
    success_url = '/top/#contact'

    def get_context_data(self, **kwargs):
        """
        news ニュースのデータ
        usage 使用例のデータ
        """
        context = super().get_context_data(**kwargs)
        news = News.objects.using('db_help').all().order_by('-date')
        usages = UsageExamples.objects.using('db_help').all()
        context['news'] = news
        context['usages'] = usages
        return context
    
    def form_valid(self, form):
        # get the token submitted in the form
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(payload).encode()
        req = urllib.request.Request(url, data=data)

        # verify the token submitted with the form is valid
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        # result will be a dict containing 'success' and 'action'.
        # it is important to verify both

#        if (not result['success']) or (not result['action'] == 'homepage'):  # make sure action matches the one from your template
#            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.お手数ですが、もう一度送信し直してください。')
#            return super().form_invalid(form)
        return self.send_to_me()

    def send_to_me(self):
        form = ContactForm(self.request.POST)
        if form.is_valid():
            subject = self.request.POST['subject']
            message = self.request.POST['email']+'からのメールです.\n'+self.request.POST['content']
            from_email = self.request.POST['email']
            recipient_list = ["kutskhrk.convolution123@gmail.com"]

            send_mail(subject, message, from_email, recipient_list)
            messages.success(self.request, '送信が成功しました')
        return redirect(self.get_success_url())


class NewsView(TemplateView):
    """News Page"""
    template_name='help/news.html'

    def get_context_data(self, **kwargs):
        """
        news ニュースのデータ
        """
        context = super().get_context_data(**kwargs)
        news = News.objects.using('db_help').get(id=self.kwargs['pk'])
        context['news'] = news
        return context
    
