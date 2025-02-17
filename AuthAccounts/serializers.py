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
        fields = ['first_name',  'last_name', 'date_of_birth', 'gender', 'email','password']
