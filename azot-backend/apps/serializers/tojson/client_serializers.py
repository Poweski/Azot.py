from rest_framework import serializers
from apps.serializers.tojson.client_cart_serializer import CartOutSerializer
from apps.serializers.tojson.seller_serializers import PurchaseSerializer


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
    cart = CartOutSerializer()


    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'client_info': ClientInfoOutSerializer().to_representation(instance.client_info),
            'cart': CartOutSerializer().to_representation(instance.cart),
            'purchases': PurchaseSerializer(instance.purchase_set.all(), many=True).data,
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'email': data.get('email'),
            'client_info': ClientInfoOutSerializer().to_internal_value(data.get('client_info')),
            'cart': CartOutSerializer().to_internal_value(data.get('cart')),
        }