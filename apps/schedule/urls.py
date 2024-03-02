from django.urls import path
from .views import ScheduleListAPIView, LessonDetailAPIView, AttendanceListAPIView

urlpatterns = [
    path('schedules/', ScheduleListAPIView.as_view(), name='schedule-list-create'),
    path('lessons/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
    path('attendances/', AttendanceListAPIView.as_view(), name='attendance-list'),
]
