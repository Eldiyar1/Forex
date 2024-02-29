from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Schedule(models.Model):
    date = models.DateField(verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')

    def __str__(self):
        return f'Schedule on {self.date}'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    start_time = models.TimeField(verbose_name=_('Start time'))
    end_time = models.TimeField(verbose_name=_('End time'))
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('Schedule'))

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __str__(self):
        return f'Lesson "{self.name}" on {self.schedule.date}'


class Attendance(models.Model):
    STATUS_CHOICES = [
        (1, _('Present')),
        (0, _('Absent')),
    ]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=_('Lesson'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    status = models.PositiveIntegerField(default=0, choices=STATUS_CHOICES, verbose_name=_('Status'))

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')

    def __str__(self):
        return f'Attendance of {self.user} for lesson "{self.lesson.name}"'
