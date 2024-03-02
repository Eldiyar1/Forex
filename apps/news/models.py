from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from apps.common.models import BaseModel


class News(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    image = models.ImageField(upload_to='news/images/', verbose_name=_('Image'))
    start_datetime = models.DateTimeField(verbose_name=_('Start Datetime'))

    def __str__(self):
        return str(format_lazy(_("News: {title}"), title=self.title))

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ("-created_at",)
