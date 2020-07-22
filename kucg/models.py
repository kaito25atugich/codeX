import django
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.validators import BaseValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible


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
            raise ValidationError(f'ファイルサイズは{self.key}以下にしてください. 現在のファイルサイズは{(int(value.size)/(1000*1000))}MBです.')
    
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
        help_text='appname, databaseと同じ名前をつけるべし！！上限は40文字として値はuniqueなものである', 
        max_length=40, unique=True)

    def __str__(self):
        return self.site_name

    def get_all_relation(self):
        """
        ForeignKeyで結ばれたすべてのモデルを集める。
        モデルを追加した場合には、追記する必要あり！！
        """
        news = self.news_set.all().order_by('-date')
        topimages = self.topimages_set.all()
        introduction = self.introduction_set.all()
        tag = self.tag_set.all()
        snstwitter = self.snstwitter_set.all()
        youremail = self.youremail_set.all()
        return news, topimages, introduction, tag, snstwitter, youremail


class Tag(models.Model):
    COLORS=(
        ("rgb(255, 54, 121)","pink"),
        ("rgb(42, 228, 178)","green"),
        ("rgb(68, 62, 50)","black"),
        ("rgb(250, 83, 22)","orange"),
        ("rgb(42, 42, 255)","blue"),
        ("rgb(16, 218, 233)","cyan"),
        ("rgb(223, 58, 223)","purple"),
        ("rgb(178, 236, 60)","yellowgreen"),
        ("rgb(201, 111, 9)","brown")
    )

    tag = models.CharField(verbose_name='タグ', max_length=15,unique=True, 
        help_text='※必須項目です。また、名前は他のものとかぶらないものにしてください。'
    )
    color = models.CharField(verbose_name='色',max_length=20,choices=COLORS,default="rgb(255, 54, 121)",null=True,
        help_text='色を選択してください。もし選択しなかった場合はpinkになります。'
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    
    def text_return(self):
        if len(self.tag) <= 6:
            return self.tag
        return self.tag[0:6]+"..."

    def __str__(self):
        return self.tag
    
    def return_model_name(self):
        """モデルを説明する言葉"""
        return "ニュースのタグ"

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
        return  self.tag, self.color, self.site


class News(models.Model):
    """
    Newsモデル
    title タイトル
    tag 活動内容か動画か新入生用か選択　
    message ニュース本体
    movie　動画
    img  画像
    date 日付
    site どのサイトに対して紐づけるか
    動画か画像は片方一方のみでいきたい
    """

    title = models.CharField(verbose_name='タイトル', max_length=30,
        help_text='※必須項目です。ニュースのタイトルを入力してください。最大30文字です'
    )
    tag = models.ManyToManyField(Tag,verbose_name="Tag",
        help_text='※必須項目です。タグがない場合は先に作成してください。CtrlもしくはCommandキーで複数選択できます。'
    )
    message = models.TextField(verbose_name='ニュース', blank=True, 
        help_text='ニュースの内容を入力してください。'
    )
    img = models.ImageField(verbose_name='記事の画像', upload_to='images',blank=True, null=True,
        help_text='画像ファイルをアップロードできます。アップロードされた画像はサムネ、記事のトップに表示できます。',
        validators=[UploadSizeValidator(settings.MAX_UPLOAD_SIZE)]
    )
    mov = models.FileField(verbose_name="記事の動画",upload_to='movies',blank=True,null=True,
        help_text='動画ファイルをアップロードできます。ファイルサイズは最大500MBまでです。',
        validators=[FileExtensionValidator(['mp4',]),UploadSizeValidator(settings.MAX_UPLOAD_SIZE)]
    )
    date = models.DateTimeField(default=django.utils.timezone.now)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)


    def __str__(self):
        tag = self.tag.all()
        tags = []
        for t in tag:
            tags.append(t)
        return f'{self.date}: {self.title}: {tags}'
    
    def return_model_name(self):
        """モデルを説明する言葉"""
        return "ニュース"

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
        return True

    def name_of_many_models(self):
        """ManyToManyFieldを設定したmodel名をリターンする"""
        return ('tag',)

    def return_all_element(self):
        """すべてのモデルをリターンする"""
        return self.title, self.tag, self.message, self.img, self.movie, self.date, self.site


class Comment(models.Model):
    news = models.ForeignKey(News,verbose_name='Article',on_delete=models.CASCADE)
    name  = models.CharField(verbose_name='名前', max_length=30, blank=True,default="Commenter")
    comment = models.CharField(verbose_name='コメント', max_length=300, blank=True)
    date = models.DateTimeField(default=django.utils.timezone.now)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}: {self.news.title}'



class TopImages(models.Model):
    """
    サイト最上部に表示する画像モデル
    form にて一枚しか登録できないようにしている.
    top_img 画像本体
    top_alt 画像がない時に代わりに表示する
    site どのサイトに対して紐づけるか
    """
    id = models.IntegerField(primary_key=True, auto_created=True, validators=[MaxNumImages(1)],
            help_text='画像を識別するための番号です。0より大きく1以下の値を設定してください。'
        )
    img = models.ImageField(verbose_name='Top画像', upload_to='images',blank=True, null=True,
        help_text='Top画像をアップロードできます。投稿できるのは一枚までです。',
        validators=[UploadSizeValidator(settings.MAX_UPLOAD_SIZE)]
    )
    top_alt = models.CharField(verbose_name='Top画像のalt', max_length=140,
        help_text='画像を言葉で説明するために必要な項目です。140字以内で入力してください。', 
        default='画像')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.top_alt
    
    def return_model_name(self):
        """モデルを説明する言葉"""
        return "トップ画像"

    def is_file_img(self):
        """画像ファイルを含んでいるか"""
        return True

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
        return 3
    
    def check_many_field(self):
        """ManyToManyFieldを持っているか確認する"""
        return False

    def return_all_element(self):
        """すべてのモデルをリターンする"""
        return self.id, self.img, self.top_alt, self.site


class Introduction(models.Model):
    """
    サークルの紹介の画像、紹介文のモデル
    img 紹介者の画像
    introducer 紹介者の名前
    intro_alt 紹介文
    site どのサイトに対して紐づけるか
    """
    id = models.IntegerField(primary_key=True, auto_created=True, validators=[MaxNumImages(1)],
        help_text='画像を識別するための番号です。0より大きく1以下の値を設定してください。'
    )
    img = models.ImageField(verbose_name='紹介者の画像', upload_to='images',blank=True, null=True,
        help_text='サークル紹介のプロフィール画像を変更できます。アップロードできるのは一枚までです。',
        validators=[UploadSizeValidator(settings.MAX_UPLOAD_SIZE)]
    )
    introducer = models.CharField(verbose_name="紹介者の名前",max_length=15,
        help_text="サークル紹介者の名前です。15字以内で入力してください",default="紹介者")
    introduce = models.CharField(verbose_name='紹介文', max_length=200,
        help_text='サークルの紹介文です。200字以内で入力してください。', 
        default='画像')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.introducer

    def return_model_name(self):
        """モデルを説明する言葉"""
        return "紹介文"

    def is_file_img(self):
        """画像ファイルを含んでいるか"""
        return True

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
        return 4
    
    def check_many_field(self):
        """ManyToManyFieldを持っているか確認する"""
        return False

    def return_all_element(self):
        """すべてのモデルをリターンする"""
        return self.id, self.img, self.introduce, self.introducer, self.site


class SNSTwitter(models.Model):
    """
    Twitteのリンクモデル
    id 識別番号
    url Twitterのリンク
    """
    id = models.IntegerField(primary_key=True, auto_created=True, validators=[MaxNumImages(1)],
            help_text='画像を識別するための番号です。0より大きく1以下の値を設定してください。'
        )
    url = models.URLField(verbose_name='TwitterのURL',
        help_text='Twitterのリンクを入力して下さい。最大で一つまで入力できます。'
        )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.url
    
    def return_model_name(self):
        """モデルを説明する言葉"""
        return "Twitterへのリンク"

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
        return 5
    
    def check_many_field(self):
        """ManyToManyFieldを持っているか確認する"""
        return False

    def return_all_element(self):
        """すべてのモデルをリターンする"""
        return self.id, self.url, self.site


class YourEmail(models.Model):
    """
    Emailアドレス設定用モデル
    id 識別番号
    email メールアドレス
    secure　securetoken
    """
    id = models.IntegerField(primary_key=True, auto_created=True, validators=[MaxNumImages(1)],
        help_text='画像を識別するための番号です。0より大きく1以下の値を設定してください。'
        )
    email = models.EmailField(verbose_name='メールアドレス',
        help_text='メールアドレスを入力して下さい。最大で一つまで作成できます。'
        )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
    
    def return_model_name(self):
        """モデルを説明する言葉"""
        return "メールアドレスの設定"

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
        return 6
    
    def check_many_field(self):
        """ManyToManyFieldを持っているか確認する"""
        return False

    def return_all_element(self):
        """すべてのモデルをリターンする"""
        return self.id, self.email, self.site