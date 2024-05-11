import uuid

from apps.models import Client, Product, Seller, ClientInfo, SellerInfo
from rest_framework import serializers


class ClientInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return Client.objects.create(id=uuid.uuid4(),
                                     email=validated_data.get('email'),
                                     password=validated_data.get('password'),
                                     client_info=ClientInfo.objects.create()
                                     )

    def update(self, instance, validated_data):
        instance.id = uuid.uuid4()
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class ClientOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'email': data.get('email'),
        }


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


class ClientInfoOutSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def to_representation(self, instance):
        return {
            'name': instance.name,
            'surname': instance.surname,
            'phone': instance.phone,
            'address': instance.address,
            'balance': instance.balance,
        }

    def to_internal_value(self, data):
        return {
            'name': data.get('name'),
            'surname': data.get('surname'),
            'phone': data.get('phone'),
            'address': data.get('address'),
            'balance': data.get('balance'),
        }


class ClientOutWithInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    client_info = ClientInfoOutSerializer()

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'client_info': ClientInfoOutSerializer().to_representation(instance.client_info),
        }

    def to_internal_value(self, data):
        return {
            'email': data.get('email'),
            'client_info': ClientInfoOutSerializer().to_internal_value(data.get('client_info')),
        }


class SellerInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        return Seller.objects.create(id=uuid.uuid4(),
                                     email=validated_data.get('email'),
                                     password=validated_data.get('password'),
                                     seller_info=SellerInfo.objects.create()
                                     )

    def update(self, instance, validated_data):
        instance.id = uuid.uuid4()
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class SellerOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'email': data.get('email'),
        }


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


class SellerInfoOutSerializer(serializers.Serializer):
    organization = serializers.CharField()
    phone = serializers.CharField()
    address = serializers.CharField()

    def to_representation(self, instance):
        return {
            'organization': instance.organization,
            'phone': instance.phone,
            'address': instance.address,
        }

    def to_internal_value(self, data):
        return {
            'organization': data.get('organization'),
            'phone': data.get('phone'),
            'address': data.get('address'),
        }


class SellerOutWithInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()
    seller_info = SellerInfoOutSerializer()

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'seller_info': SellerInfoOutSerializer().to_representation(instance.seller_info),
        }

    def to_internal_value(self, data):
        return {
            'email': data.get('email'),
            'seller_info': SellerInfoOutSerializer().to_internal_value(data.get('seller_info')),
        }


class ProductInSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    image = serializers.URLField()

    def create(self, validated_data, *args, **kwargs):
        return Product.objects.create(id=uuid.uuid4(),
                                      name=validated_data.get('name'),
                                      price=validated_data.get('price'),
                                      description=validated_data.get('description'),
                                      image=validated_data.get('image'),
                                      seller=args[0])

    def update(self, instance, validated_data, *args, **kwargs):
        instance.id = uuid.uuid4()
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        seller = args[0]
        instance.seller = seller
        instance.save()
        return instance


class ProductOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    image = serializers.URLField()
    seller = SellerOutWithInfoSerializer()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'price': instance.price,
            'description': instance.description,
            'image': instance.image,
            'seller': SellerOutWithInfoSerializer().to_representation(instance.seller),
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'name': data.get('name'),
            'price': data.get('price'),
            'description': data.get('description'),
            'image': data.get('image'),
            'seller': SellerOutWithInfoSerializer().to_internal_value(data.get('seller')),
        }
