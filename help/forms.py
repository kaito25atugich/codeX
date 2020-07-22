from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import News
from .models import UsageExamples


class ContactForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'text-form'}))
    email = forms.EmailField(label='メールアドレス', required=True, widget=forms.EmailInput(attrs={'class': 'email-form'}))
    subject = forms.CharField(label='件名', max_length=80, required=True, widget=forms.TextInput(attrs={'class': 'text-form'}))
    content = forms.CharField(label='お問い合わせ内容', max_length=2000, required=True, widget=forms.Textarea(attrs={'class': 'textarea-form'}))


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


class Form2(forms.ModelForm):
    """
    UsageExamples Form
    """
    class Meta:
        model = UsageExamples
        fields = ('id', 'title', 'description', 'mov', 'img')

    form2_change_or_not = forms.BooleanField(label='使用例に変更を加える場合はチェックを入れてください。', 
        required=False,
        initial=False,
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs["class"] = "text-form"
        self.fields['description'].widget.attrs["class"] = "text-form"
    
    def return_model_name(self):
        return '使用例'