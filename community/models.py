from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
import secrets

User = get_user_model()

import secrets
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

def generate_group_id():
    return secrets.token_hex(8).upper() # Generate a unique 16-character hex ID

class ChatRoom(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='created_chatrooms'  # Better query reverse access
    )
    open = models.BooleanField(default=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    group_name =  models.CharField(max_length=200, blank=True, null=True, db_index=True)  # Index for faster lookups

    # More collision-resistant ID (8-char hex, but consider 12+ for scalability)
    chat_id = models.CharField(
        max_length=16,
        unique=True,
        editable=False,
        default=generate_group_id  # e.g., "A1B2C3D4"
    )

    general = models.BooleanField(default=False)  # System-created group?
    group = models.BooleanField(default=False)

    users = models.ManyToManyField(
        to=User,
        related_name='chat_members',
        blank=True
    )

    city = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        db_index=True  # Faster filtering
    )

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure group_id is unique on creation
        if not self.chat_id:
            self.chat_id = secrets.token_hex(8).upper()


    def __str__(self):
        return f"ChatRoom {self.chat_id} ({'Open' if self.open else 'Closed'})"


class RoomMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, to_field='chat_id', on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()

    is_question = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    is_answer = models.BooleanField(default=False)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.chat_room.creator.pk} {self.user.username}'
