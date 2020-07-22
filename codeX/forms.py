from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].widget.attrs["class"] = "text-form"
        self.fields['username'].widget.attrs["class"] = "text-form"
        self.fields['email'].widget.attrs["class"] = "text-form"


class CodexPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'pass-form'


