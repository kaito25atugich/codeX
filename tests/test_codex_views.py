from datetime import datetime
from datetime import timedelta
from datetime import timezone

from django.test import Client
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from django_hosts.resolvers import reverse as h_reverse

from codeX.models import Site
from codeX.models import User

from help.models import News
from help.models import UsageExamples
from help.models import Site as HelpSite


class ViewTest(TestCase):
    databases = ('default', 'db_help')
    def setUp(self):
        self.date = '2020-4-1 12:00'
        self.password = 'test'
        self.u = User.objects.using('default').create(user_id='555', password='test', email='test@test.com', username='shark', is_staff = True, is_admin = True)
        self.site = Site.objects.using('default').create(site_name='help', url='help.convolution.xyz:8000/top/', user=self.u)
        self.client = Client()
        self.c_site = HelpSite.objects.using('db_help').create(url='help.convolution.xyz:8000/top/', site_name='help')
        self.news = News.objects.using('db_help').create(title='コロナ', date=self.date, site=self.c_site)
        self.usage = UsageExamples.objects.using('db_help').create(id=1, title='たいとる',site=self.c_site)

    def test_get(self):
        """getで通常のアクセスを行う."""
        response = self.client.get(reverse('codeX:top'))
        self.assertEqual(response.status_code, 200)

    def test_get_login(self):
        response = self.client.get(reverse('codeX:login'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        self.client.login(user_id=self.u.user_id, password=self.password)

    def test_get_edit(self):
        response = self.client.get(reverse('codeX:edit', kwargs={'pk':1, }))
        self.assertEqual(response.status_code, 302)

    def test_login_edit(self):
        self.client.force_login(self.u)
        response = self.client.get(reverse('codeX:edit', kwargs={'pk':1, }))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_edit(self):
        self.client.force_login(self.u)
        self.client.logout()
        response = self.client.get(reverse('codeX:edit', kwargs={'pk':1, }))
        self.assertNotEqual(response.status_code, 200)
    
    def test_get_update(self):
        response = self.client.get(reverse('codeX:update', kwargs={'pk':1, }))
        self.assertEqual(response.status_code, 302)

    def test_login_update(self):
        self.client.force_login(self.u)
        response = self.client.get(reverse('codeX:update', kwargs={'pk':1, }))
        self.assertEqual(response.status_code, 200)

    def test_logout_update(self):
        self.client.force_login(self.u)
        self.client.logout()
        response = self.client.get(reverse('codeX:update', kwargs={'pk':1, }))
        self.assertNotEqual(response.status_code, 200)
        
    def test_get_update_page(self):
        response = self.client.get(reverse('codeX:update_page', kwargs={'pk':1,'mod_id':1,'mod':'News',}))
        self.assertEqual(response.status_code, 302)
    
    def test_login_update_page(self):
        self.client.force_login(self.u)
        response = self.client.get(reverse('codeX:update_page', kwargs={'pk':1,'mod_id':1,'mod':'News',}))
        news = News.objects.using('db_help').filter(id=1)
        self.assertQuerysetEqual(
            news, ['<News: 2020-04-01 03:00:00+00:00: コロナ>']
        )
        self.assertEqual(response.status_code, 200)
    
    def test_logout_update_page(self):
        self.client.force_login(self.u)
        self.client.logout()
        response = self.client.get(reverse('codeX:update_page', kwargs={'pk':1,'mod_id':1,'mod':'News',}))
        self.assertNotEqual(response.status_code, 200)
    
    def test_function_update_page(self):
        self.client.force_login(self.u)
        data = {
            'title': 'コロナだよ',
            'date': self.date,
            'content': 'kkkk',
        }
        response = self.client.post(reverse('codeX:update_page', kwargs={'pk':1,'mod_id':1,'mod':'News',}), data)
        self.assertEqual(response.status_code, 302)
        self.news.refresh_from_db()
        news = News.objects.using('db_help').filter(id=1)
        self.assertQuerysetEqual(
            news, ['<News: 2020-04-01 03:00:00+00:00: コロナだよ>']
        )
    
    def test_get_delete(self):
        COUNT = 1
        response = self.client.get(reverse('codeX:delete', kwargs={'pk':1,'mod_id':1,'mod':'News',}))
        self.assertEqual(News.objects.using('db_help').all().count(), COUNT)
        self.assertEqual(response.status_code, 302)

    def test_login_delete(self):
        COUNT = 0
        self.client.force_login(self.u)
        response = self.client.get(reverse('codeX:delete', kwargs={'pk':1,'mod_id':1,'mod':'News',}))
        self.assertEqual(News.objects.using('db_help').all().count(), COUNT)

    def test_logout_delete(self):
        COUNT = 1
        self.client.force_login(self.u)
        self.client.logout()
        response = self.client.get(reverse('codeX:delete', kwargs={'pk':1,'mod_id':1,'mod':'News',}))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(News.objects.using('db_help').all().count(), COUNT)

    def test_get_profile(self):
        response = self.client.get(reverse('codeX:profile'))
        self.assertEqual(response.status_code, 302)

    def test_login_profile(self):
        self.client.force_login(self.u)
        response = self.client.get(reverse('codeX:profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_profile(self):
        self.client.force_login(self.u)
        self.client.logout()
        response = self.client.get(reverse('codeX:profile'))
        self.assertEqual(response.status_code, 302)