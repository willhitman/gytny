# community/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from .consumers import CommunityChatConsumer
from core.middleware import WebSocketJWTAuthMiddleware

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_id>\d+)/$', CommunityChatConsumer.as_asgi()),
]

#👌keep it frosty
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebSocketJWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
