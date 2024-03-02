from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models import User, Profile


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=6, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    phone = PhoneNumberField(region='KG')

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["token"]


# class UserProfileSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username')
#     email = serializers.CharField(source='user.email')
#
#     class Meta:
#         model = Profile
#         fields = ['id', 'username', 'email', 'avatar']
#         read_only_fields = ['user']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    phone = PhoneNumberField(source='user.phone', region='KG', required=False)

    class Meta:
        model = Profile
        fields = ['user', 'avatar', 'username', 'phone', 'email']
        read_only_fields = ['user', 'email']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return instance

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
