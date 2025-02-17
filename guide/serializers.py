from django.db import transaction
from rest_framework.serializers import ModelSerializer

from guide.models import Guide, Address, Route


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'province', 'city', 'surburd', 'postal_code']


class CreateGuideSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Guide
        fields = ['user', 'address']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        guide = Guide.objects.create(address=address, **validated_data)
        return guide

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address

        for attr, value in address_data.items():
            setattr(address, attr, value)
        address.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class GetRoutesSerializers(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Route
        fields = ['guide', 'address', 'taxi_rank_name', 'bus_stop', 'fare', 'likes', 'dislikes', 'shares',
                  'date_created', 'last_updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = {
            'users': [like.user.username for like in instance.likes.all()],
            'count': instance.likes.count()
        }
        representation['dislikes'] = {
            'users': [dislike.user.username for dislike in instance.dislikes.all()],
            'count': instance.dislikes.count()
        }
        representation['shares'] = {
            'users': [share.user.username for share in instance.shares.all()],
            'count': instance.shares.count()
        }
        return representation


class CreateRouteSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Route
        fields = ['guide', 'address', 'taxi_rank_name', 'bus_stop', 'fare', ]

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        with transaction.atomic():
            address = Address.objects.create(**address_data)
            guide = Route.objects.create(address=address, **validated_data)
            return guide


    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address

        for attr, value in address_data.items():
            setattr(address, attr, value)
        address.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
