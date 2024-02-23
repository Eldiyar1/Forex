from django.db.models import Avg
from rest_framework import generics, filters

from .models import Course, Lecture, Review
from .serializers import CourseListSerializer, CourseDetailSerializer, LectureSerializer, ReviewSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    serializer_class = CourseListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.select_related('author') \
        .prefetch_related('reviews', 'lectures').annotate(avg_rating=Avg('reviews__rating'))
    serializer_class = CourseDetailSerializer


class LectureListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lecture.objects.all().select_related('course')
    serializer_class = LectureSerializer


class LectureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all().select_related('course')
    serializer_class = LectureSerializer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all().select_related('course', 'user')
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().select_related('course', 'user')
    serializer_class = ReviewSerializer
