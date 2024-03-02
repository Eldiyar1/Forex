from django.urls import path
from .views import CourseListCreateAPIView, CourseDetailAPIView, ReviewListCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
]
