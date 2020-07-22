from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


alphanumeric = RegexValidator(r'^[0-9a-zA-Z_-]*$', 'Only alphanumeric characters are allowed.')


class UserManager(BaseUserManager):
    def create_user(self, user_id, email, password, **extra):
        if not user_id and email:
            raise ValueError('user_idまたはemailは必須項目です')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            user_id=user_id,
            **extra,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_user(self, user_id, email, password=None, **extra):
        """一般ユーザの管理権限をなくす"""
        extra.setdefault('is_superuser', False)
        extra.setdefault('is_staff', False)
        return self.create_user(user_id, email,password, **extra)
    
    def create_superuser(self, user_id, email, password, **extra):
        """管理ユーザの作成"""
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_staff', True)
        if extra.get('is_staff') is not True:
            raise ValueError('Superuser must have the right is_staff')
        if extra.get('is_superuser') is not True:
            raise ValueError('Superuser must have the right is_superuser')
        return self.create_user(user_id, email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    """model of user"""
    user_id = models.CharField(verbose_name='user ID', unique=True, max_length=15, help_text='あなたを識別するために必要な項目です。15字以下の英数字で入力してください。', validators=[alphanumeric])
    email = models.EmailField(verbose_name='email')
    username = models.CharField(verbose_name='username', max_length=50, help_text='必須項目です。あなたのチーム名を50字以下で入力してください。')
    is_staff = models.BooleanField(verbose_name='staff', default=False,
    help_text=('weather the user can log into admin site')
    )
    is_active = models.BooleanField(verbose_name='staff status', default=True,
        help_text=('whether the user is active or not'),
    )
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'username']


    def __str__(self):
        return self.user_id + ': ' + self.username

class Site(models.Model):
    site_name = models.CharField(verbose_name='サイト名', max_length=40)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.site_name
