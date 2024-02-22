import os

import cv2
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
from django.http import JsonResponse
from django.utils.text import format_lazy
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from cors.settings.base import AUTH_USER_MODEL


class Course(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    image = models.ImageField(upload_to='courses/images/', verbose_name=_('Image'))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Price'))
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses',
                               verbose_name=_('Author'))

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ("-created_at",)

    def __str__(self):
        return str(format_lazy(_("Course '{title}' by {author}"), title=self.title, author=self.author))


class Lecture(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures', verbose_name=_('Course'))
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    part_number = models.FloatField(validators=[MinValueValidator(0)], verbose_name=_('Part Number'))
    duration = models.FloatField(
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        verbose_name=_('Duration'),
        help_text=_('Optional'),
    )
    video_file = models.FileField(
        upload_to='lectures/video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'webm']), ],
        verbose_name=_('Video File'),
        help_text=_('Supported formats: mp4, mov, avi, webm'),
    )

    class Meta:
        verbose_name = _('Lecture')
        verbose_name_plural = _('Lectures')
        ordering = ("-created_at",)

    def __str__(self):
        return str(format_lazy(_("Part {part_number}: {title}"), part_number=self.part_number, title=self.title))

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
                    return JsonResponse({"error": _("Error processing video file: ") + str(e)},
                                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return JsonResponse({"error": _("Video file not found.")}, status=status.HTTP_404_NOT_FOUND)


class Review(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Course'))
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews',
                             verbose_name=_('User'))
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name=_('Rating'))
    comment = models.TextField(verbose_name=_('Comment'))
    created_at = models.DateField(auto_now_add=True, verbose_name=_('Date Created'))

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ("-created_at",)

    def __str__(self):
        return str(format_lazy(_("Review from {user} for {course_title} - Rating: {rating}"), user=self.user,
                               course_title=self.course.title, rating=self.rating))
