from django.db.models import Count, Prefetch, Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.schedule.models import Schedule, Lesson, Attendance, User
from apps.schedule.serializers import ScheduleSerializer, LessonSerializer, AttendanceSerializer


class ScheduleListCreateAPIView(ListCreateAPIView):
    queryset = Schedule.objects.all().prefetch_related('lessons')
    serializer_class = ScheduleSerializer


class ScheduleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all().prefetch_related('lessons')
    serializer_class = ScheduleSerializer


class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all().prefetch_related('attendances')
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all().prefetch_related('attendances')
    serializer_class = LessonSerializer


class BaseAttendanceAPIView:
    queryset = Attendance.objects.all().select_related('lesson').prefetch_related(
        Prefetch('user', queryset=User.objects.annotate(
            total_attendances=Count('attendances', filter=Q(attendances__status=1))
        ))
    )
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Attendance.objects.filter(user=user)


class AttendanceListCreateAPIView(BaseAttendanceAPIView, ListCreateAPIView):
    pass


class AttendanceRetrieveUpdateDestroyAPIView(BaseAttendanceAPIView, RetrieveUpdateDestroyAPIView):
    pass
