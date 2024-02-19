from rest_framework import serializers
from .models import Course, Lecture, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'course', 'rating', 'comment', 'created_at')
        read_only_fields = ('user',)


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'part_number', 'title', 'duration', 'video_file')


class BaseCourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'title', 'image', 'price', 'rating')

    def get_rating(self, obj):
        return obj.avg_rating if obj.avg_rating is not None else None


class CourseListSerializer(BaseCourseSerializer):
    class Meta(BaseCourseSerializer.Meta):
        model = Course


class CourseDetailSerializer(BaseCourseSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    lectures = LectureSerializer(many=True, read_only=True)
    total_duration = serializers.SerializerMethodField()
    lecture_count = serializers.SerializerMethodField()

    class Meta(BaseCourseSerializer.Meta):
        model = Course
        fields = BaseCourseSerializer.Meta.fields + ('total_duration', 'lecture_count', 'lectures', 'reviews')
        read_only_fields = ('author',)

    def get_total_duration(self, obj):
        total_duration = sum(lecture.duration for lecture in obj.lectures.all() if lecture.duration)
        return int(total_duration)

    def get_lecture_count(self, obj):
        return obj.lectures.count()

