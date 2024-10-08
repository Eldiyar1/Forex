from django.db.models import Avg, Prefetch
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import Course, Review
from .serializers import CourseListSerializer, CourseDetailSerializer, ReviewSerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    serializer_class = CourseListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('title',)
    ordering_fields = ('avg_rating', 'price')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.prefetch_related(
        Prefetch('lectures'),
        Prefetch('reviews', queryset=Review.objects.select_related('user__profile')),
        'author__profile'
    ).select_related('author__profile').annotate(avg_rating=Avg('reviews__rating'))

    serializer_class = CourseDetailSerializer


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all().select_related('course', 'user')
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().select_related('course', 'user')
    serializer_class = ReviewSerializer
