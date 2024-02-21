import os

import cv2
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
from django.utils.text import format_lazy
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from cors.settings.base import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Название'))
    image = models.ImageField(upload_to='courses/images/', verbose_name=_('Изображение'))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Цена'))
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses',
                               verbose_name=_('Автор'))

    class Meta:
        verbose_name = _('Курс')
        verbose_name_plural = _('Курсы')

    def __str__(self):
        return str(format_lazy(_("Курс '{title}' от {author}"), title=self.title, author=self.author))


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', verbose_name=_('Курс'))
    title = models.CharField(max_length=200, verbose_name=_('Название'))
    part_number = models.FloatField(validators=[MinValueValidator(0)], verbose_name=_('Номер части'))
    duration = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name=_('Продолжительность'),
        help_text=_('Не обязательно к заполнению'),
    )
    video_file = models.FileField(
        upload_to='lectures/video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'webm']), ],
        verbose_name=_('Видеофайл'),
        help_text=_('Поддерживаемые форматы: mp4, mov, avi webm'),
    )

    class Meta:
        verbose_name = _('Лекция')
        verbose_name_plural = _('Лекции')

    def __str__(self):
        return str(format_lazy(_("Часть {part_number}: {title}"), part_number=self.part_number, title=self.title))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.video_file:
            video_path = os.path.join(settings.MEDIA_ROOT, str(self.video_file))
            if os.path.exists(video_path):
                try:
                    cap = cv2.VideoCapture(video_path)
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.duration = round(frame_count / fps, 2)
                    Lecture.objects.filter(pk=self.pk).update(duration=self.duration)
                except Exception as e:
                    return Response({"error": f"Error processing video file: {e}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Video file not found."}, status=status.HTTP_404_NOT_FOUND)


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Курс'))
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews',
                             verbose_name=_('Пользователь'))
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Рейтинг'))
    comment = models.TextField(verbose_name=_('Комментарий'))
    created_at = models.DateField(auto_now_add=True, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    def __str__(self):
        return str(format_lazy(_("Отзыв от {user} для {course_title} - Рейтинг: {rating}"), user=self.user,
                               course_title=self.course.title, rating=self.rating))
