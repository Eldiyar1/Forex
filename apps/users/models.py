from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150, blank=False, null=False, unique=True, verbose_name=_("логин")
    )
    password = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_("password")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("активирован?"))
    is_staff = models.BooleanField(default=False, verbose_name=_("сотрудник?"))
    is_superuser = models.BooleanField(
        default=False, verbose_name=_("админ пользователь?")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-created_at",)
