from django.contrib import admin
from .models import Schedule, Lesson, Attendance


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'schedule')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'status')
