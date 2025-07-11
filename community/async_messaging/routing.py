from django.urls import re_path

from community.async_messaging.consumers import CommunityChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<chat_id>[0-9A-F]{16})/$', CommunityChatConsumer.as_asgi()),
]