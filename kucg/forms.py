from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Comment
from .models import Introduction
from .models import News
from .models import Tag
from .models import TopImages
from .models import SNSTwitter
from .models import YourEmail




class Form1(forms.ModelForm):
    """
    Tag Form
    """
    class Meta:
        model = Tag
        fields = ('tag', 'color')
        
    form1_change_or_not = forms.BooleanField(label='ニュースのタグに変更を加える場合はチェックを入れてください。', 
        required=False,
        initial=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].widget.attrs["class"] = "text-form"
        self.fields['color'].widget.attrs["class"] = "text-form"

    def return_model_name(self):
        return 'ニュースのタグ'



class Form2(forms.ModelForm):
    """
    News Form
    """
    class Meta:
        model = News
        fields = ('title','tag','message','img','mov','date')
        widgets = {
                'message': SummernoteWidget()
        }
         
    form2_change_or_not = forms.BooleanField(label='ニュースに変更を加える場合はチェックを入れてください。', 
        required=False,
        initial=False,
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs["class"] = "text-form"
        self.fields['tag'].widget.attrs["class"] = "text-form"
        self.fields['date'].widget.attrs["class"] = "text-form"

    def return_model_name(self):
        return 'ニュース'


    
class Form3(forms.ModelForm):
    """
    TopImages Form
    """
    class Meta:
        model = TopImages
        fields = ('id', 'img', 'top_alt')
        
        
    form3_change_or_not = forms.BooleanField(
        label='トップ画像を変更する場合はチェックを入れてください。',
        required=False,
        initial=False,
        )   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['top_alt'].widget.attrs["class"] = "text-form"
    
    def return_model_name(self):
        return 'トップ画像'


class Form4(forms.ModelForm):
    """
    Introduction Form
    """
    class Meta:
        model = Introduction
        fields = ('id', 'img', 'introducer', 'introduce')
        widgets = {
                'introduce': SummernoteWidget(),
        }
        
    form4_change_or_not = forms.BooleanField(
        label='紹介文を変更する場合はチェックを入れてください。',
        required=False,
        initial=False,
        )   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['introducer'].widget.attrs["class"] = "text-form"

    def return_model_name(self):
        return '紹介文'


class Form5(forms.ModelForm):
    """
    SNSTwitter Form
    """
    class Meta:
        model = SNSTwitter
        fields = ('id', 'url')
        
    form5_change_or_not = forms.BooleanField(
        label='Twitterへのリンクを変更する場合はチェックを入れてください。',
        required=False,
        initial=False,
        )   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs["class"] = "text-form"

    def return_model_name(self):
        return 'Twitterへのリンク'

    
class Form6(forms.ModelForm):
    """
    YourEmail Form
    """
    class Meta:
        model = YourEmail
        fields = ('id', 'email')
        
    form6_change_or_not = forms.BooleanField(
        label='メールアドレスの設定を変更する場合はチェックを入れてください。',
        required=False,
        initial=False,
        )   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs["class"] = "email-form"

    def return_model_name(self):
        return 'メールアドレスの設定'