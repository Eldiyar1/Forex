# serializers.py
from django.db.models import Avg
from rest_framework import serializers
from .models import Course, Lecture, Review


class ReviewSerializer(serializers.ModelSerializer):
    rating_stars = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating_stars', 'comment', 'created_at']

    def get_rating_stars(self, obj):
        stars = "★" * obj.rating
        return stars


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'duration', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    lectures = LectureSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'image', 'price', 'rating', 'total_duration', 'reviews', 'lectures']

    def get_rating(self, obj):
        rating_avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        if rating_avg is None:
            return "Пока нет рейтинга"
        else:
            stars = "★" * int(round(rating_avg))
            return stars

    def get_total_duration(self, obj):
        return sum(lecture.duration for lecture in obj.lectures.all())
