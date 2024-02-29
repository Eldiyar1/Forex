from rest_framework import serializers
from .models import Schedule, Lesson, Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    attendances = AttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'
