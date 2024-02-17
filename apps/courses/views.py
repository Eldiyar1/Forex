from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Course, Lecture, Review
from .serializers import CourseSerializer, LectureSerializer, ReviewSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all().prefetch_related('reviews', 'lectures')
    serializer_class = CourseSerializer


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all().prefetch_related('reviews', 'lectures')
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

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)

        if Review.objects.filter(course=course, user=user).exists():
            return Response({"error": "Пользователь уже оставил отзыв для этого курса"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().select_related('course', 'user')
    serializer_class = ReviewSerializer
