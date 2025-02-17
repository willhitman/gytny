# community/urls.py
from django.urls import path
from .views import WebSocketInfoView, CreateChatRoomView

urlpatterns = [
    path('api/websocket-info/', WebSocketInfoView.as_view(), name='websocket-info'),
    path('api/create-room/', CreateChatRoomView.as_view(), name='create-room'),
]