from django.db.models import Count
from rest_framework import serializers
from .models import Schedule, Lesson, Attendance, Homework
from ..users.models import User


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'name', 'description', 'deadline', 'homework')
        abstract = True


class LessonSerializer(serializers.ModelSerializer):
    homeworks = HomeWorkSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'start_time', 'end_time', 'homeworks')


class LessonWithoutHomeWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'start_time', 'end_time')
        abstract = True


class ScheduleSerializer(serializers.ModelSerializer):
    lessons = LessonWithoutHomeWorksSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = ('id', 'date', 'lessons')


class UserSerializer(serializers.ModelSerializer):
    total_attendances = serializers.SerializerMethodField()

    @staticmethod
    def get_total_attendances(obj):
        return obj.attendances.filter(status=1).aggregate(total_attendances=Count('id'))['total_attendances']

    class Meta:
        model = User
        fields = ('id', 'username', 'total_attendances')
        abstract = True


class AttendanceSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'status', 'lesson', 'user', 'schedule']
