# community/urls.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from .async_messaging.routing import websocket_urlpatterns
from .views import WebSocketInfoView, CreateChatRoomView, GetChatRoomsView

urlpatterns = [
    path('api/websocket-info/', WebSocketInfoView.as_view(), name='websocket-info'),
    path('api/create-room/', CreateChatRoomView.as_view(), name='create-room'),
    path('api/get-rooms/', GetChatRoomsView.as_view(), name='get-rooms'),
]

