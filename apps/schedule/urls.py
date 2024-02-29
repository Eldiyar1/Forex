from django.urls import path
from .views import ScheduleListCreateAPIView, ScheduleRetrieveUpdateDestroyAPIView, LessonListCreateAPIView, \
    LessonRetrieveUpdateDestroyAPIView, AttendanceListCreateAPIView, AttendanceRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('schedules/', ScheduleListCreateAPIView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', ScheduleRetrieveUpdateDestroyAPIView.as_view(), name='schedule-detail'),
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
    path('attendances/', AttendanceListCreateAPIView.as_view(), name='attendance-list'),
    path('attendances/<int:pk>/', AttendanceRetrieveUpdateDestroyAPIView.as_view(), name='attendance-detail'),
]
