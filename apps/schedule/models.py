from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy

from apps.common.models import BaseModel

User = get_user_model()


class Schedule(BaseModel):
    date = models.DateField(verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')
        ordering = ("-created_at",)

    def __str__(self):
        return str(format_lazy(_("Schedule on {date}"), date=self.date))


class Homework(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    homework = models.FileField(upload_to='homeworks/files/', verbose_name=_('Homework'))
    schedule = models.ForeignKey(Schedule, models.CASCADE, related_name='homeworks', verbose_name=_('Schedule'))

    class Meta:
        verbose_name = _('Homework')
        verbose_name_plural = _('Homeworks')
        ordering = ("-created_at",)

    def __str__(self):
        return str(format_lazy(_("Homework \"{name}\""), name=self.name))


class Lesson(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    start_time = models.TimeField(verbose_name=_('Start time'))
    end_time = models.TimeField(verbose_name=_('End time'))
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('Schedule'))

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __str__(self):
        return str(format_lazy(_("Lesson \"{name}\" on {date}"), name=self.name, date=self.schedule.date))


class Attendance(BaseModel):
    STATUS_CHOICES = [
        (1, 1),
        (0, 0),
    ]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances', verbose_name=_('Lesson'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances', verbose_name=_('User'))
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES, verbose_name=_('Status'))
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendances',
                                 verbose_name=_('Schedule'))

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')
        ordering = ("-created_at",)

    def __str__(self):
        return str(
            format_lazy(_("Attendance of {user} for lesson \"{lesson}\""), user=self.user, lesson=self.lesson.name))
