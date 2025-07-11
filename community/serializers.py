from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from AuthAccounts.models import User
from community.models import ChatRoom, RoomMessage


class CreatorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name']


class CreateChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['users', 'group']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['creator'] = instance.creator.username
        representation['chat_id'] = instance.chat_id
        representation['open'] = instance.open
        representation['closed_at'] = instance.closed_at
        representation['date_created'] = instance.date_created
        representation['last_updated'] = instance.last_updated
        return representation


class GetChatRoomSerializer(ModelSerializer):
    creator = CreatorSerializer()

    class Meta:
        model = ChatRoom
        exclude = ['date_created', 'last_updated']




class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CreateMessageSerializer(ModelSerializer):


    class Meta:
        model = RoomMessage
        fields = ['chat_room', 'user', 'message', 'is_question', 'is_answer', 'is_answered', 'parent']




class RoomMessageSerializer(ModelSerializer):

    user = serializers.StringRelatedField()
    replies = RecursiveSerializer(many=True, read_only=True)
    parent_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = RoomMessage
        fields = [
            'id', 'user', 'message', 'is_question',
            'is_answer', 'is_answered', 'date_created',
            'replies', 'parent_id'
        ]
