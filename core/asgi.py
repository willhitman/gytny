# myproject/asgi.py
import os

import django

import community

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from community.async_messaging import routing
from community.async_messaging.routing import websocket_urlpatterns
from core.middleware import WebSocketJWTAuthMiddleware


''' django socket not preconfigured to work with jwt late alone reading headers so we need to create a 
middleware to do that '''
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebSocketJWTAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                community.async_messaging.routing.websocket_urlpatterns
            )
        )
    ),
})

