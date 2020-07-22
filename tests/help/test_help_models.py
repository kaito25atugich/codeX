from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from help.models import News
from help.models import Site
from help.models import UsageExamples


class TestModels(TestCase):
    databases = ('default', 'db_help')
    def setUp(self):
        self.site = Site.objects.create(url='ttt.com', site_name='pr')
        self.date = '2020-4-1 12:00'
        News.objects.create(title='コロナ', site=self.site, date=self.date)
        UsageExamples.objects.create(id=1, title='たいとる',site=self.site)
        self.news = News.objects.get(id=1)
        self.usage = UsageExamples.objects.get(id=1)

    def test_is_file_img(self):
        self.assertFalse(self.news.is_file_img())
        self.assertTrue(self.usage.is_file_img())

    def test_is_file_mov(self):
        self.assertFalse(self.news.is_file_mov())
        self.assertTrue(self.usage.is_file_mov())

    def test_can_edit(self):
        self.assertTrue(self.news.can_edit())
        self.assertTrue(self.usage.can_edit())

    def test_can_delete(self):
        self.assertTrue(self.news.can_delete())
        self.assertTrue(self.usage.can_delete())

    def test_can_update(self):
        self.assertTrue(self.news.can_update())
        self.assertTrue(self.usage.can_update())

    def test_confirm_form_num(self):
        self.assertEqual(self.news.confirm_form_num(), 1)
        self.assertEqual(self.usage.confirm_form_num(), 2)
    
    def test_return_all_element(self):
        self.assertEqual(str(self.news.return_all_element()), "('コロナ', datetime.datetime(2020, 4, 1, 3, 0, tzinfo=<UTC>), None, <Site: pr>)")
        self.assertEqual(str(self.usage.return_all_element()), "(1, 'たいとる', None, <FieldFile: None>, <ImageFieldFile: None>, <Site: pr>)")

    def test_upper_limit_usage(self):
        UsageExamples.objects.create(id=4, title='たいとる',site=self.site)
        self.assertRaises(ValidationError)

    def test_lower_limit_usage(self):
        UsageExamples.objects.create(id=-1, title='たいとる',site=self.site)
        self.assertRaises(ValidationError)