from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from community.models import ChatRoom, RoomMessage, Content


class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['creator']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['creator'] = instance.creator.username
        representation['open'] = instance.open
        representation['closed_at'] = instance.closed_at
        representation['date_created'] = instance.date_created
        representation['last_updated'] = instance.last_updated
        return representation


class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = ['current_location', 'destination', 'distance', 'price']


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CreateMessageSerializer(ModelSerializer):
    content = ContentSerializer()

    class Meta:
        model = RoomMessage
        fields = ['chat_room', 'user', 'description', 'is_question', 'is_answer', 'is_answered', 'content', 'parent']

    def save(self, **kwargs):
        content_data = self.validated_data.pop('content')
        content = Content.objects.create(**content_data)
        message = RoomMessage.objects.create(content=content, **self.validated_data)
        return message


class RoomMessageSerializer(ModelSerializer):
    content = ContentSerializer()
    user = serializers.StringRelatedField()
    replies = RecursiveSerializer(many=True, read_only=True)
    parent_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = RoomMessage
        fields = [
            'id', 'user', 'description', 'is_question',
            'is_answer', 'is_answered', 'content', 'date_created',
            'replies', 'parent_id'
        ]
