import secrets
import string
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
from django.utils import timezone

def generate_user_id():
    return secrets.token_hex(9).upper()

# Create your models here.
class User(AbstractUser):
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )

    ROLES = (
        ('ADMIN', 'ADMIN'),
        ('USER', 'USER'),
    )

    username = models.CharField(max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=254, unique=True, default="server@gytny.co.za")

    user_id = models.CharField(
        max_length=18,
        unique=True,
        editable=False,
        default=generate_user_id,
    )

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True, choices=GENDER)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    socials = models.ManyToManyField('UserSocials', blank=True)

    role = models.CharField(max_length=10, choices=ROLES, default='USER')

    city = models.CharField(max_length=100, blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    verification_pin = models.CharField(max_length=6, blank=True, null=True)
    token_created_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def generate_verification_pin(self):
        digits = string.digits
        secure_random = secrets.SystemRandom()
        pin = ''.join(secure_random.choice(digits) for _ in range(6))
        self.verification_pin = pin
        return self.verification_pin

    def is_token_valid(self):
        if not self.token_created_at:
            return False
        expiration_time = self.token_created_at + timezone.timedelta(hours=24)
        return timezone.now() <= expiration_time

    def verify_user(self):
        self.is_verified = True
        self.save()
        return self

    def __str__(self):
        return f'{self.username}'



class UserSocials(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.link}'


class UserAccountPasswordResetPin(models.Model):
    user = models.ForeignKey(
        to=User,
        to_field='user_id',
        on_delete = models.CASCADE,
        blank=True,
        null = True,
        related_name='user_pins')

    pin = models.CharField(max_length=6, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def generate_verification_pin(self):
        digits = string.digits
        secure_random = secrets.SystemRandom()
        pin = ''.join(secure_random.choice(digits) for _ in range(6))
        self.pin = pin
        return self.pin

    def is_pin_valid(self):
        if not self.last_updated:
            return False
        expiration_time = self.last_updated + timezone.timedelta(hours=3)
        return timezone.now() <= expiration_time


    def __str__(self):
        return f'{self.user.username} {self.user.user_id}'


