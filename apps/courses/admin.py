from django.contrib import admin
from .models import Course, Lecture, Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title', 'video_url')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration')
    list_filter = ('course',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('course', 'user')
    search_fields = ('course__title', 'user__username')
