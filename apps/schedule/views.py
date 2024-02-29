from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count

from apps.schedule.models import Schedule, Lesson, Attendance
from apps.schedule.serializers import ScheduleSerializer, LessonSerializer, AttendanceSerializer


class ScheduleListCreateAPIView(ListCreateAPIView):
    queryset = Schedule.objects.all().select_related('lessons')
    serializer_class = ScheduleSerializer


class ScheduleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all().select_related('lessons')
    serializer_class = ScheduleSerializer


class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all().prefetch_related('attendances')
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().prefetch_related('attendances')
    serializer_class = LessonSerializer


class AttendanceListCreateAPIView(ListCreateAPIView):
    queryset = Attendance.objects.all().select_related('lesson', 'user').annotate(total_attendance=Count('id'))
    serializer_class = AttendanceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttendanceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all().select_related('lesson', 'user')
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        return super().get_queryset().annotate(total_attendance=Count('id'))
