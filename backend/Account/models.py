import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')

        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_employee = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("メールアドレス", max_length=255, unique=True)
    last_name = models.CharField("苗字", default="顧客", max_length=20)
    first_name = models.CharField("名前", default="太郎", max_length=20)
    last_name_kana = models.CharField("苗字カナ", default="コキャク", max_length=30)
    first_name_kana = models.CharField("名前カナ", default="タロウ", max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'last_name_kana', 'first_name_kana']

    def __str__(self):
        return self.email


class ManageUser(models.Model):
    # 1~5までのパーミッションlevel
    permission_level = models.IntegerField(default=1)
