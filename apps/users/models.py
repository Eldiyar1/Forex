from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True, verbose_name=_("Логин"))
    email = models.EmailField(max_length=100, null=True, verbose_name=_("Почта"))
    phone = PhoneNumberField(null=True, blank=False, unique=True, verbose_name=_("Номер телефона"))
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Пароль"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активирован?"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Сотрудник?"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Админ пользователь?"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("-created_at",)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    avatar = models.ImageField(null=True, blank=False, verbose_name=_("Аватар"))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Профиль")
        verbose_name_plural = _("Профили")
