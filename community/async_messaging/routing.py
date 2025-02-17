# community/routing.py
from django.urls import re_path
from .consumers import CommunityChatConsumer

websocket_urlpatterns = [
    # Example URL: ws://localhost:8000/ws/community_chat/1/
    re_path(r'^ws/chat/(?P<room_id>\d+)/$', CommunityChatConsumer.as_asgi()),
]
