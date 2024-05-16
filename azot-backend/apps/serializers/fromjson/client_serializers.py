import uuid

from rest_framework import serializers
from apps.models import Client, ClientInfo, Cart


class ClientInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return Client.objects.create(id=uuid.uuid4(),
                                     email=validated_data.get('email'),
                                     password=validated_data.get('password'),
                                     client_info=ClientInfo.objects.create(),
                                     cart=Cart.objects.create()
                                     )

    def update(self, instance, validated_data):
        instance.id = uuid.uuid4()
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class ClientInfoInSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        return ClientInfo.objects.create(name=validated_data.get('name'),
                                         surname=validated_data.get('surname'),
                                         phone=validated_data.get('phone'),
                                         address=validated_data.get('address'),
                                         balance=0.0)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance