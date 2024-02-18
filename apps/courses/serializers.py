from rest_framework import serializers
from .models import Course, Lecture, Review


class ReviewSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title')

    class Meta:
        model = Review
        fields = ('id', 'user', 'course_title', 'rating', 'comment', 'created_at')


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'title', 'duration', 'video_file')


class CourseSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    lectures = LectureSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Course

        fields = (
            'id', 'title', 'image', 'price', 'rating', 'total_duration', 'reviews', 'lectures', 'author', 'author_name'
        )

    def get_rating(self, obj):
        return obj.avg_rating if obj.avg_rating is not None else "Пока нет рейтинга"

    def get_total_duration(self, obj):
        total_duration = sum(lecture.duration for lecture in obj.lectures.all() if lecture.duration)
        return int(total_duration)

    def get_author_name(self, obj):
        return obj.author.username
