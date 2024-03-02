from django.urls import path

from apps.users import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('confirm/', views.VerifyOTP.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileUserAPIView.as_view(), name='login'),
    path('change_password/', views.ChangePasswordView.as_view(), name='login'),
    path(
        "reset-password-email/",
        views.ResetPasswordSendEmail.as_view(),
        name="search user and send mail",
    ),
    path("reset-password-code/", views.PasswordResetCode.as_view(), name="write code"),
    path(
        "reset-new-password/<str:code>/",
        views.PasswordResetNewPassword.as_view(),
        name="write new password",
    ),
]
