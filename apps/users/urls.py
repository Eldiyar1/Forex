from django.urls import path

from apps.users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileUserAPIView.as_view(), name='login'),
    path('change_password/', views.ChangePasswordView.as_view(), name='login')
]
