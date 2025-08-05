import json

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import User, UserAccountPasswordResetPin
from AuthAccounts.serializers import UserCreateSerializer, ForgotPasswordSerializer, ForgotPasswordResetSerializer
from mailing.background_tasks import send_verification_email, send_password_reset_pin_email


def verify_email(user):
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # check and generate verification token if none is found
        if not user.verification_token:
            user.generate_verification_token()
            user.save()
        # Now send the token
        send_verification_email.delay(user.email, user.verification_token)
        return True


class CreateAccountView(GenericAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def __init__(self):
        super().__init__()
        self.user = None

    def post(self, request):
        user_data = {
            'first_name': request.data.get('first_name') or None,
            'last_name': request.data.get('last_name') or None,
            'username': request.data.get('username') or None,
            'gender': request.data.get('gender') or None,
            'email': request.data.get('email') or None,
            'password': request.data.get('password') or None
        }

        serializer = self.serializer_class(data=user_data, partial=True)
        if serializer.is_valid():
            self.user = User.objects.create(**serializer.validated_data )
            self.user.set_password(serializer.validated_data['password'])
            self.user.generate_verification_token()
            self.user.save()
            result = verify_email(self.user)
            if not result:
                self.user.delete()
                return Response({'error': 'Verification email could not be sent'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                send_verification_email.delay(self.user.email, self.user.verification_token)
            return Response({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class ForgotPasswordResetCodeView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    throttle_classes = [AnonRateThrottle]

    def post(self, request, **kwargs):

        email = request.data.get("email") or None
        if email:
            user = self.queryset.filter(email=email).first()
            if user and not user.is_verified:
               _user, created = UserAccountPasswordResetPin.objects.get_or_create(user_id=user.user_id)
               if _user.is_pin_valid():
                   return Response({'message':'Check your email, you have an active pin'}, status=status.HTTP_304_NOT_MODIFIED)
               else:
                   _user.generate_verification_pin()
                   _user.save()
               send_password_reset_pin_email(email=email,pin=_user.pin)
            else:
                return Response({'error': 'Either account is not verified or doesnt exist'},
                                status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Email address required'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordResetView(GenericAPIView):
    serializer_class = ForgotPasswordResetSerializer
    permission_classes = [AllowAny]
    queryset = UserAccountPasswordResetPin.objects.all()
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            try:
                _user = self.queryset.get(pin=serializer.validated_data['pin'])
            except UserAccountPasswordResetPin.DoesNotExist:
                return Response({'error':'Code is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if _user.is_pin_valid():
                    try:
                        user = User.objects.get(user_id=_user.user_id)
                    except User.DoesNotExist:
                        return Response({'error':'User not found'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        password = serializer.validated_data['password']
                        password_confirm = serializer.validated_data['password_confirm_field']

                        if password == password_confirm:
                            user.set_password(password)
                            user.save()
                            return Response({'message':'User password updated successfully'},
                                            status=status.HTTP_200_OK)
                        return Response({'error':'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error':'This pin has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

