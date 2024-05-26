from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager
from ..common.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=150, blank=False, null=False, unique=True, verbose_name=_("Username"))
    email = models.EmailField(null=True, verbose_name=_("E-mail"))
    phone = PhoneNumberField(null=True, blank=False, unique=True, verbose_name=_("Phone Number"))
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Password"))
    otp = models.CharField(max_length=4, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=False, verbose_name=_("Active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Admin"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Created'))
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-created_at",)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    avatar = models.ImageField(null=True, blank=False, verbose_name=_("Avatar"))

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "profile"
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("-created_at",)


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    time = models.DateTimeField()
