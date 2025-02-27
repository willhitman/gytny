# community/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from .consumers import CommunityChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_id>\d+)/$', CommunityChatConsumer.as_asgi()),
]

#👌keep it frosty
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
