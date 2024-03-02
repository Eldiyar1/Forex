from rest_framework.generics import ListAPIView

from apps.schedule.models import Schedule, Lesson, Attendance
from apps.schedule.serializers import ScheduleSerializer, LessonSerializer, AttendanceSerializer


class ScheduleListCreateAPIView(ListAPIView):
    queryset = Schedule.objects.all().prefetch_related('lessons')
    serializer_class = ScheduleSerializer


class LessonListCreateAPIView(ListAPIView):
    queryset = Lesson.objects.all().prefetch_related('attendances')
    serializer_class = LessonSerializer


class AttendanceListCreateAPIView(ListAPIView):
    queryset = Attendance.objects.all().select_related('lesson')
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(user=user)
