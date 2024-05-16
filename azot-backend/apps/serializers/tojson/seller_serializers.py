from rest_framework import serializers


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

