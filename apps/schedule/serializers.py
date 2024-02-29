from django.db.models import Count
from rest_framework import serializers
from .models import Schedule, Lesson, Attendance
from ..users.models import User


class UserSerializer(serializers.ModelSerializer):
    total_attendances = serializers.SerializerMethodField()

    @staticmethod
    def get_total_attendances(obj):
        return obj.attendances.filter(status=1).aggregate(total_attendances=Count('id'))['total_attendances']

    class Meta:
        model = User
        fields = ('id', 'username', 'total_attendances')


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'status', 'lesson', 'user']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'start_time', 'end_time', 'schedule')


class ScheduleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = ('id', 'date', 'lessons')
