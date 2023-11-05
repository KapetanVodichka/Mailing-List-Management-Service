from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, null=True)
    phone = models.CharField(max_length=30, verbose_name='телефон', blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name='страна', blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    is_superuser = models.BooleanField(default=False, verbose_name='Админ')
    is_manager = models.BooleanField(default=False, verbose_name='Менеджер')
    code = models.CharField(default=None, verbose_name='код верификации', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
