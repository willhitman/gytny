# myproject/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from community.async_messaging import routing
from community.async_messaging.routing import websocket_urlpatterns
from core.middleware import WebSocketJWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

''' django socket not preconfigured to work with jwt late alone reading headers so we need to create a 
middleware to do that '''
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        WebSocketJWTAuthMiddleware(  # Apply the middleware
            URLRouter(websocket_urlpatterns)
        )
    ),
})

