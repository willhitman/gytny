from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from AuthAccounts.models import User


class UserAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)

            if not user.is_active:
                return None

            pwd_valid = check_password(password, user.password)
            if pwd_valid:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
