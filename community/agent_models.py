from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    open = models.BooleanField(default=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.creator.pk}'


class RoomMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, null=True, blank=True, related_name='listing')

    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='content', blank=True, null=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.chat_room.creator.pk} {self.user.username}'

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    listing = models.BooleanField(default=False)

    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='content', blank=True, null=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.chat_room.creator.pk} {self.user.username}'

class Content(models.Model):

    TYPE =[
        ('HOUSE', 'House'),
        ('APARTMENT', 'Apartment'),
        ('LAND', 'Land'),
        ('COMMERCIAL', 'Commercial'),
        ('OTHER', 'Other')
    ]

    city = models.CharField(max_length=200, blank=True, null=True)
    section = models.CharField(max_length=200, blank=True, null=True)

    price = models.FloatField(default=0.00, blank=True, null=True)
    land_size = models.FloatField(default=0.00, blank=True, null=True)
    floor_size = models.FloatField(default=0.00, blank=True, null=True)
    bedrooms = models.IntegerField(default=0, blank=True, null=True)
    bathrooms = models.IntegerField(default=0, blank=True, null=True)
    garages = models.IntegerField(default=0, blank=True, null=True)
    type = models.CharField(max_length=100, choices=TYPE, blank=True, null=True)

    link = models.CharField(max_length=500, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.city} {self.section}'
