from typing import Type

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.schedule.filters import ScheduleFilter
from apps.schedule.models import Schedule, Lesson, Attendance
from apps.schedule.serializers import ScheduleSerializer, LessonSerializer, AttendanceSerializer


class ScheduleListAPIView(ListAPIView):
    queryset = Schedule.objects.all().prefetch_related('lessons')
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class: Type[ScheduleFilter] = ScheduleFilter


class LessonDetailAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all().prefetch_related('attendances')
    serializer_class = LessonSerializer


class AttendanceListAPIView(ListAPIView):
    queryset = Attendance.objects.all().select_related('lesson')
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(user=user)
