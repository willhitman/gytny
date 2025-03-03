
from django.urls import re_path
from .consumers import CommunityChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_id>\d+)/$', CommunityChatConsumer.as_asgi()),
]


