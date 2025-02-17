from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from community.models import ChatRoom
from community.serializers import CreateRoomSerializer


class WebSocketInfoView(APIView):
    @swagger_auto_schema(
        operation_description="Provides the WebSocket URL for the community chat.",
        responses={
            200: openapi.Response(
                description="WebSocket connection details",
                examples={
                    "application/json": {
                        "websocket_url": "ws://localhost:8000/ws/community_chat/{room_id}/"
                    }
                },
            )
        }
    )
    def get(self, request):
        return Response({
            "websocket_url": "ws://localhost:8000/ws/community_chat/{room_id}/"
        })


class CreateChatRoomView(CreateAPIView):
    serializer_class = CreateRoomSerializer
    permission_classes = []
    queryset = ChatRoom.objects.all()


