from django.test import Client
from django.test import TestCase
from django.test import RequestFactory
from django_hosts.resolvers import reverse

from help.models import News
from help.models import UsageExamples
from help.models import Site


class TestViews(TestCase):
    databases = {'db_help'}
    def setUp(self):
        self.site = Site.objects.using('db_help').create(url='help.convolution.xyz:8000', site_name='help')
        self.date = '2020-4-1 12:00'
        self.news = News.objects.using('db_help').create(title='コロナ', date=self.date, site=self.site, need_page=True)
        self.usage = UsageExamples.objects.using('db_help').create(id=1, title='たいとる', site=self.site)
        
    # def test_get_top(self):
    #     response = self.client.get(reverse('top', host='help'))
    #     self.assertEqual(response.status_code, 200)

    # def test_get_news(self):
    #     response = self.client.get(reverse('news', host='help', kwargs={'pk':1}))
    #     self.assertEqual(response.status_code, 200)
    
    def test_get_model(self):
        COUNT = 1
        self.assertEqual(News.objects.using('db_help').all().count(), COUNT)

    
