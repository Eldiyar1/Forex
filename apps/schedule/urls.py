from django.urls import path
from .views import ScheduleListCreateAPIView, LessonListCreateAPIView, AttendanceListCreateAPIView

urlpatterns = [
    path('schedules/', ScheduleListCreateAPIView.as_view(), name='schedule-list-create'),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list'),
    path('attendances/', AttendanceListCreateAPIView.as_view(), name='attendance-list'),
]
