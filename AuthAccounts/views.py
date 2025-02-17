import json

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from AuthAccounts.serializers import UserCreateSerializer


class CreateAccountView(GenericAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = {
            'first_name': None if request.data.get('first_name') == '' else request.data.get('first_name'),
            'last_name': None if request.data.get('last_name') == '' else request.data.get('last_name'),
            'username': None if request.data.get('email') == '' else request.data.get('email'),
            'gender': None if request.data.get('gender') == '' else request.data.get('gender'),
            'email': None if request.data.get('email') == '' else request.data.get('email'),
            'password': None if request.data.get('password') == '' else request.data.get('password')
        }

        serializer = self.serializer_class(data=user_data, partial=True)
        if serializer.is_valid():
            user = User.objects.create(**serializer.data, )
            user.username = serializer.validated_data['email']
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
