import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


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

    username = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=50, blank=True, null=True, unique=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True, null=True, choices=GENDER)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    socials = models.ManyToManyField('UserSocials', blank=True)

    role = models.CharField(max_length=10, choices=ROLES, default='USER')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return f'{self.username}'


class UserSocials(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.link}'


