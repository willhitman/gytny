from asgiref.sync import sync_to_async
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

    is_question = models.BooleanField(default=False)
    is_answer = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)

    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='content', blank=True, null=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.chat_room.creator.pk} {self.user.username}'


class Content(models.Model):
    current_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)

    distance = models.FloatField(default=0.00, blank=True, null=True)
    price = models.FloatField()

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.current_location} {self.destination}'
