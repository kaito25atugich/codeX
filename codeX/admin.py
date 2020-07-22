from django.contrib import admin

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import Site
from .models import User
# Register your models here.


class UserCreationForm(forms.ModelForm):
    """新しいユーザーを作る.繰り返しパスワードもプラスして"""
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('user_id', 'email', 'username')


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")
        return password2


    def save(self, commit=True):
        """ハッシュ化して保存"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()


    class Meta:
        models = User
        fields = ('user_id', 'email', 'username')
    
    def clean_password(self):
        return self.initial['password']
    

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('user_id', 'email', 'username')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('user_id',)}),
        ('Personal Info', {'fields': ('email', 'username', 'password',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('user_id','email','username','password1','password2')
        }),
    )
    search_fields = ('user_id',)
    ordering = ('user_id',)
    filter_horizontal = ()


class SiteAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        print(request.POST)
        print(form)
        obj.save()


admin.site.register(User, UserAdmin)
admin.site.register(Site, SiteAdmin)

