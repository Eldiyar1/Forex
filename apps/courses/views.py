from django.db.models import Avg
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Course, Lecture, Review
from .serializers import CourseSerializer, LectureSerializer, ReviewSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.select_related('author').prefetch_related('reviews', 'lectures').annotate(
        avg_rating=Avg('reviews__rating'))
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('title',)


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.select_related('author').prefetch_related('reviews', 'lectures').annotate(
        avg_rating=Avg('reviews__rating'))
    serializer_class = CourseSerializer


class LectureListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lecture.objects.all().select_related('course')
    serializer_class = LectureSerializer


class LectureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all().select_related('course')
    serializer_class = LectureSerializer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all().select_related('course', 'user')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Вы должны быть аутентифицированы, чтобы оставить отзыв."},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().select_related('course', 'user')
    serializer_class = ReviewSerializer
