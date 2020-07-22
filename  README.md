### CodeXとは

フォーム送信を用いたWebサイト更新アプリケーションである。
HTMLでページを作成し、変更が見込まれる部分についてModelを作成し各アプリケーションのデータベースにて保存する。
各アプリケーションのModelにはSiteモデルがありこのモデルと同様のものがCodeX側にも用意されており、このSiteモデルが同じであることを利用し可能な限りの汎用性を実現している。

### 使用方法

1. 新たに使用したいアプリケーション(Webページ)を作成する。データベース名はdb_<app_name>としてsettings.pyに追加すること。その後にrouter.pyで設定を行う。また、サブドメインを用いたい場合には、django_hostsをつかった設定が可能である。以下settings.pyにおいてsqlite3を用いたデータベースの設定を行う例。

```python
  DATABASES = {  
  	'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.default.sqlite3'),
        'TEST': {
            'NAME': 'test_default',
            'DEPENDENCIES': [],
        },
    },
    'db_help': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.db_help.sqlite3'),
        'TEST': {
            'DEPENDENCIES': ['default',],
        },
    },
  }
```

2. アプリケーション内にてmodelを作成し、作成したmodelについてforms.py内に各formを作成する。

例：注意点で定義されたNewsモデルについてFormを作成する例

```python
class Form1(forms.ModelForm):
    """
    News Form
    """
    class Meta:
        model = News
        fields = ('title', 'date', 'content', 'need_page')
        widgets = {
            'content': SummernoteWidget(),
        }
        
    form1_change_or_not = forms.BooleanField(label='お知らせに変更を加える場合はチェックを入れてください。', 
        required=False,
        initial=False,
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs["class"] = "text-form"
        self.fields['date'].widget.attrs["class"] = "text-form"
    
    def return_model_name(self):
        return 'お知らせ'
```

**各モデルのForm名はForm\<NUM\>とすること **(NUM：1から昇順でつける。これをしないとエラーが起こる)

また必ずform\<NUM\>_change_or_notの要素を追加すること。edit(新規作成機能において必要となる。)

3. CodeXでユーザーを作成し、サイトと結びつける。

### 注意点

#### model
はじめに、各アプリケーションのmodelには必ずSiteモデルを作成する。
構成要素として以下の二つのカラム、二つのメソッドが必要。

- カラム
  -  url: サイトのurl
  -  site_name: サイトの名前(はじめに設定したapp名と同様のものを用いる。以下に詳しく記述するが、database名にも用いる)
- メソッド
  - str: adminサイトで確認しやすくする
  - get_all_relation: CodeXに反映したいモデルについて記述する必要がある。例としてNewsというモデルを以下のように定義した場合

```python
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

```

get_all_relationメソッドでは以下のような記述を行う。

```python
def get_all_relation(self):
        """
        ForeignKeyで結ばれたすべてのモデルを集める。

        モデルを追加した場合には、追記する必要あり。
        """
        news = self.news_set.all().order_by('-date')
       
        return news
```

次に、各モデルについてであるが、上記のNewsモデルのようにモデルの構成に必要な項目を入力ののち**必ず以下の項目を入力**する必要がある。

カラム

- Site: どのサイトに属するモデルかを明確にするために導入している。これにより先述のget_all_relationで逆参照することができる。

メソッドについては各メソッドごとに紹介を入れているので詳細は省くが上記Newsモデルにて定義されているメソッドは全て入力する必要がある。いくつかのメソッドについてだけ説明をするとreturn_model_nameには任意の文字を入力することが可能である。confirm_form_numで用いられるform番号はforms.py内にて設定したものと同値のものを返すとよい。



ストレージにs3を用いたためboto3などが入っているがアプリケーションと同層もしくは同端末内の別ディレクトリで保存する場合には削除する必要がある。

### Contributor

Kaito (https://github.com/kaito25atugich)

Saka-rinta (https://github.com/saka-rinta)