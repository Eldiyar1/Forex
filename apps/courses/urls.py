from django.urls import path
from .views import CourseListAPIView, CourseDetailAPIView, ReviewListCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
]
