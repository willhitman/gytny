from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db.models import Prefetch
from django.utils import timezone
from community.models import ChatRoom, RoomMessage
import json
from community.serializers import CreateMessageSerializer, RoomMessageSerializer
from community.async_messaging.protol_buffer import incoming_message_pb2

class CommunityChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.user = None
        self.chat_id = None

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']



        self.user = self.scope["user"]

        if isinstance(self.user, AnonymousUser):
            await self.close(code=403, reason="User not authenticated")  # Reject unauthenticated users
            return

        # 🚶‍♀️‍➡️Join the room group
        await self.channel_layer.group_add(
            self.chat_id,
            self.channel_name
        )
        await self.accept()

        # Send room status and history on connect
        self.room = await self.get_room()

        if self.room:
            history = await self.get_message_history()
            await self.send(text_data=json.dumps({
                'type': 'room_status',
                'is_closed': not self.room.open,
                'history': history
            }))
        else:
            await self.close(code=4000, reason="Room is either closed or does not exist")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'message':
            await self.handle_message(data)
        elif action == 'close_room':
            await self.handle_close_room()
        elif action == 'typing':
            await self.handle_typing(data)

    async def handle_message(self, data):

        if self.room and self.room.open:
            # Check if this message is a reply by looking for a parent_id
            parent_id = data.get('parent_id') if data.get('parent_id') else None

            #Todo check if message is not null in the future and also check if content exists

            message = {
                'user': self.user.pk,
                'chat_room': self.chat_id,
                'message': data['message'],
                "is_question": data['is_question'],
                "is_answered": data['is_answered'],
                "is_answer": data['is_answer'],
                'parent': parent_id
            }
            message = await self.create_message(message, parent_id)

            await self.channel_layer.group_send(
                self.chat_id,
                {
                    "type": "chat_message",  # This triggers `chat_message` method
                    "body": {
                        "id": message.id,
                        "user": message.user.user_id,
                        "chat_room": message.chat_room.chat_id,
                        "message": message.message,
                        "is_question": message.is_question,
                        "is_answered": message.is_answered,
                        "is_answer": message.is_answer,
                        "parent_id": message.parent.id if message.parent else None,
                        "timestamp": message.date_created.strftime("%Y-%m-%d %H:%M:%S") if message.date_created else None
                    }
                }
            )

    async def handle_typing(self, data):
        await self.channel_layer.group_send(
            self.chat_id,
            {
                "type": "typing_event",
                "user": self.user.username
            }
        )

    async def typing_event(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user": event['user']
        }))

    async def handle_close_room(self):
        room = await self.get_room()
        if room and room.creator == self.user:
            room = await self.close_room()
            await self.channel_layer.group_send(
                self.chat_id,
                {
                    'type': 'room_closed',
                    'closed_by': self.user.username,
                    # 'closed_at': room.closed_at.strftime("%Y-%m-%d %H:%M:%S") if room.closed_at else None
                }
            )

    # --- Database Operations ---
    @database_sync_to_async
    def get_room(self):
        return ChatRoom.objects.select_related("creator").filter(chat_id=self.chat_id, open=True).first()

    @database_sync_to_async
    def get_message_history(self):
        # Get all questions and their entire reply trees
        questions = RoomMessage.objects.filter(
            chat_room__chat_id=self.chat_id,
        ).order_by('pk').prefetch_related(
            Prefetch('replies',
                     queryset=RoomMessage.objects.prefetch_related(
                         Prefetch('replies',
                                  queryset=RoomMessage.objects.all(),
                                  to_attr='nested_replies')
                     ),
                     to_attr='direct_replies'
                     )
        ).select_related('user')

        # Serialize with proper nesting
        return RoomMessageSerializer(questions, many=True).data

    @database_sync_to_async
    def create_message(self, content, parent_id=None):
        serializer = CreateMessageSerializer(data=content)
        if serializer.is_valid():
            message = serializer.save()
        else:
            raise NotImplementedError(f"Invalid data: {serializer.errors}")

        if parent_id:
            try:
                parent_message = RoomMessage.objects.get(id=parent_id)
                message.parent = parent_message
                message.save()
            except RoomMessage.DoesNotExist:
                # If the parent doesn't exist, we simply leave it as a top-level message.
                raise NotImplementedError(f"Parent message {parent_id} does not exist.")
        return message

    @database_sync_to_async
    def close_room(self):
        ChatRoom.objects.filter(id=self.room_id).update(
            open=False,
            closed_at=timezone.now()
        )
        return ChatRoom.objects.get(id=self.room_id)

    # --- Group Message Handlers ---
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['body'], ensure_ascii=False))

    async def room_closed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'room_closed',
            'message': f"Room closed by {event['closed_by']}",
            'closed_at': event['closed_at'].strftime("%Y-%m-%d %H:%M:%S") if event['closed_at'] else None
        }))
