from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.utils.translation import gettext as _

from apps.users.models import User, Profile
from apps.users.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer


# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


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
                    "access_token": str(access)
                }
            )
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'username or password incorrect!'})

    def list(self, request):
        return Response(status=status.HTTP_200_OK)


class ProfileUserAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user.id)
