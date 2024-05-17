import uuid

from rest_framework import serializers
from apps.models import Seller, SellerInfo

class SellerInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return Seller.objects.create(id=uuid.uuid4(),
                                     email=validated_data.get('email'),
                                     password=validated_data.get('password'),
                                     seller_info=SellerInfo.objects.create(),
                                     )

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class SellerInfoInSerializer(serializers.Serializer):
    organization = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        return SellerInfo.objects.create(organization=validated_data.get('organization'),
                                         phone=validated_data.get('phone'),
                                         address=validated_data.get('address')
                                         )

    def update(self, instance, validated_data):
        instance.organization = validated_data.get('organization', instance.organization)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance