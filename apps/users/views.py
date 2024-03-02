import random
import string
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.utils.translation import gettext as _
from django.utils import timezone

from apps.users.email import send_email_confirmation, send_email_reset_password
from apps.users.models import Profile, User, PasswordResetToken
from apps.users.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, PasswordChangeSerializer, \
    VerifySerializer, PasswordResetSearchUserSerializer, PasswordResetCodeSerializer, PasswordResetNewPasswordSerializer


def generate_random_code(length=4):
    characters = string.octdigits + string.digits
    return "".join(random.choice(characters) for _ in range(length))


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        headers = self.get_success_headers(serializer.data)
        send_email_confirmation(user.email)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        profile = Profile.objects.create(user=user)
        profile.save()


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response(
                {
                    'messege': _('authenticate successfully'),
                    "status": status.HTTP_200_OK,
                    "username": user.username,
                    'email': user.email,
                    "refresh_token": str(refresh),
                    "access_token": str(access),
                    "access_expire": datetime.fromtimestamp(
                        access.payload.get("exp")),
                    "refresh_expire": datetime.fromtimestamp(
                        refresh.payload.get("exp")
                    ).date()
                }
            )
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'username or password incorrect!'})

    def list(self, request):
        return Response(status=status.HTTP_200_OK)


class ProfileUserAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user.id)


class ChangePasswordView(CreateAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"error": "Старый пароль указан неверно."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if old_password == new_password:
            return Response(
                {"error": "Новый пароль не должен совпадать со старым паролем."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Пароль успешно изменен."}, status=status.HTTP_200_OK
        )


class VerifyOTP(APIView):
    serializer_class = VerifySerializer

    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data.get("otp")

        user = User.objects.filter(otp=otp).first()
        if user.otp != otp:
            return Response({"error": "Неверный код подтверждения."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        user.otp = None
        user.save()
        return Response({"message": "Аккаунт успешно подтвержден."}, status=status.HTTP_200_OK)


class ResetPasswordSendEmail(CreateAPIView):
    serializer_class = PasswordResetSearchUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "Пользователь с указанным адресом электронной почты не найден."},
                            status=status.HTTP_404_NOT_FOUND)

        time = timezone.now() + timezone.timedelta(minutes=5)
        code = generate_random_code()

        password_reset_token = PasswordResetToken(user=user, code=code, time=time)
        password_reset_token.save()

        send_email_reset_password(user.email, code)

        return Response({"detail": "send"}, status=status.HTTP_200_OK)


class PasswordResetCode(CreateAPIView):
    serializer_class = PasswordResetCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        try:
            reset_token = PasswordResetToken.objects.get(code=code, time__gt=timezone.now())
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Недействительный код для сброса пароля или время истечения кода закончилось."},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response({"detail": "success", "code": code}, status=status.HTTP_200_OK)


class PasswordResetNewPassword(CreateAPIView):
    serializer_class = PasswordResetNewPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = kwargs["code"]
        password = serializer.validated_data["password"]

        try:
            password_reset_token = PasswordResetToken.objects.get(code=code, time__gt=timezone.now())
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Недействительный код для сброса пароля или время истечения кода закончилось."},
                            status=status.HTTP_404_NOT_FOUND)

        user = password_reset_token.user
        user.set_password(password)
        user.save()

        password_reset_token.delete()

        return Response({"detail": "Пароль успешно сброшен."}, status=status.HTTP_200_OK)
