from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from AuthAccounts.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['userId'] = user.id
        token['firstName'] = user.first_name
        token['lastName'] = user.last_name

        return token


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'gender', 'email']


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name',  'last_name', 'username', 'date_of_birth', 'gender', 'email','password']


class ForgotPasswordSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['email']


class ForgotPasswordResetSerializer(serializers.Serializer):

    password = serializers.CharField(allow_null=False, allow_blank=False)
    password_confirm_field = serializers.CharField(allow_null=False, allow_blank=False)
    pin = serializers.CharField(allow_null=False, allow_blank=False)

    class Meta:
        fields =['password', 'password_confirm_field', 'pin']

class VerifyUserSerializer(serializers.Serializer):
    pin = CharField(min_length=6, max_length=6, allow_null=False, allow_blank=False)
    email = serializers.EmailField(allow_null=False, allow_blank=False)

    def validate_pin(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Verification pin must only contain digits.")
        return value