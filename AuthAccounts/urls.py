from django.urls import path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
    TokenVerifySerializer
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenObtainPairView
from AuthAccounts import views


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Obtain JWT token pair (access and refresh)",
        request_body=TokenObtainPairSerializer,
        responses={200: openapi.Response('Token pair', TokenObtainPairSerializer)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Refresh JWT access token",
        request_body=TokenRefreshSerializer,
        responses={200: openapi.Response('New access token', TokenRefreshSerializer)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Verify if a given token is valid",
        request_body=TokenVerifySerializer,
        responses={200: openapi.Response('Token is valid')}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('create-account/', views.CreateAccountView.as_view(), name='create-account'),
    path('google-sso/', views.SocialLoginView.as_view(), name='google-sso'),
    path('forgot-password-code/', views.ForgotPasswordResetCodeView.as_view(), name='forgot-password-code'),
    path('forgot-password-reset/', views.ForgotPasswordResetView.as_view(), name='forgot-password-reset')

]
