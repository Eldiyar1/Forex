from django.contrib import admin
from .models import Schedule, Homework, Lesson, Attendance


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date',)
    ordering = ('-created_at',)


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'schedule', 'homework')
    ordering = ('-created_at',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'schedule')
    ordering = ('-created_at',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'status')
    ordering = ('-created_at',)
    readonly_fields = ('schedule',)
