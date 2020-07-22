import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat


@deconstructible
class MaxNumImages:
    def __init__(self, size=None):
        if size:
            self.size = size
    
    def __call__(self, value):
        if value > self.size:
            raise ValidationError(f'すでに画像の上限枚数である{self.size}枚を超えています。更新ページより現在の画像を変更してください。')
        elif value < 1:
            raise ValidationError('idには1以上の値を入力してください')

    def __eq__(self, other): 
        return (
            isinstance(other, self.__class__) and (self.size == other.size)
        )


@deconstructible
class UploadSizeValidator:
    def __init__(self, size=None):
        if size:
            self.size = size
        for key,val in settings.SIZE.items():
            if val == self.size:
                self.key = key
        
    def __call__(self, value):
        if value is None:
            return None
        if int(value.size) > int(self.size):
            raise ValidationError(f'Please keep filesize under {self.key}. Current filesize is {(int(value.size)/(1000*1000))}MB')
    
    def __eq__(self, other): 
        return (
            isinstance(other, self.__class__) and (self.size == other.size)
        )

class Site(models.Model):
    """
    Siteモデル
    url サイトのURL
    site_name サイトの名前 (注)データベースの名前、appnameと同じ名前をつけること！！！！
    """
    url = models.URLField(unique=True)
    site_name = models.CharField(verbose_name='サイト名', 
        help_text='appname, databaseと同じ名前をつけること。上限は40文字として値はuniqueなものである', 
        max_length=40, unique=True
        )

    def __str__(self):
        return self.site_name

    def get_all_relation(self):
        """
        ForeignKeyで結ばれたすべてのモデルを集める。

        モデルを追加した場合には、追記する必要あり。
        """
        news = self.news_set.all().order_by('-date')
        usage_examples = self.usageexamples_set.all()
        return news, usage_examples


class News(models.Model):
    """
    Newsモデル
    title ニュースタイトル
    content ニュース本体
    date 日付
    site どのサイトに対して紐づけるか
    """
    title = models.CharField(verbose_name='タイトル', max_length=30, 
        help_text='投稿タイトルを30文字以内で入力してください。'
    )
    date = models.DateTimeField(verbose_name='投稿日', default=timezone.now)
    content = models.TextField(verbose_name='記事内容', 
        help_text='投稿の内容を入力してください。', null=True, blank=True,
    )
    need_page = models.BooleanField(help_text='詳しくページが必要であるか、ニュース記事リンクが必要か', default=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.date}: {self.title}'
    
    def return_model_name(self):
        return 'お知らせ'

    def is_file_img(self):
        """画像ファイルを含んでいるか"""
        return False

    def is_file_mov(self):
        """動画ファイルを含んでいるか"""
        return False
    
    def can_edit(self):
        """edit で新規作成を行えるか"""
        return True

    def can_delete(self):
        """deleteを行えるようにするか"""
        return True

    def can_update(self):
        """updateを行えるようにするか"""
        return True

    def confirm_form_num(self):
        """formの番号を確認する"""
        return 1
    
    def check_many_field(self):
        """ManyToManyFieldを持っているか確認する"""
        return False

    def return_all_element(self):
        """すべてのモデルをリターンする"""
        return self.title, self.date, self.content, self.site


class UsageExamples(models.Model):
    """
    使用例のモデル
    id 最大値3とする
    title タイトル
    description 説明文
    file 動画
    example_img フロー図
    """
    id = models.IntegerField(primary_key=True, auto_created=True, validators=[MaxNumImages(3)],
        help_text='使用モデルの数を識別するための番号です。3以下の値を設定してください。'
    )
    title = models.CharField(verbose_name='タイトル', max_length=30, 
        help_text='投稿タイトルを30文字以内で入力してください。'
    )
    description = models.TextField(verbose_name='説明', max_length=1000, 
        help_text='投稿の内容。最大文字数は1000字です。', blank=True,null=True,
    )
    mov = models.FileField(verbose_name='動画ファイル', upload_to='movies/', blank=True,null=True,validators=[UploadSizeValidator(settings.MAX_UPLOAD_SIZE)])
    img = models.ImageField(verbose_name='フロー図', upload_to='images/',blank=True, null=True,validators=[UploadSizeValidator(settings.MAX_UPLOAD_SIZE)])
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.title}'
    
    def return_model_name(self):
        return '使用例'

    def is_file_img(self):
        """画像ファイルを含んでいるか"""
        return True

    def is_file_mov(self):
        """動画ファイルを含んでいるか"""
        return True
    
    def can_edit(self):
        """edit で新規作成を行えるか"""
        return True

    def can_delete(self):
        """deleteを行えるようにするか"""
        return True

    def can_update(self):
        """updateを行えるようにするか"""
        return True

    def confirm_form_num(self):
        """formの番号を確認する"""
        return 2
    
    def check_many_field(self):
        """ManyToManyFieldを持っているか確認する"""
        return False

    def return_all_element(self):
        """すべてのモデルをリターンする"""
        return self.id, self.title, self.description, self.mov, self.img, self.site
