from rest_framework import serializers
from apps.serializers.tojson.seller_serializers import SellerOutWithInfoSerializer


class ProductOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    image = serializers.URLField()
    seller = SellerOutWithInfoSerializer()
    items_available = serializers.IntegerField()
    tags = serializers.CharField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'price': instance.price,
            'description': instance.description,
            'image': instance.image,
            'seller': SellerOutWithInfoSerializer().to_representation(instance.seller),
            'items_available': instance.items_available,
            'tags': instance.tags,
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'name': data.get('name'),
            'price': data.get('price'),
            'description': data.get('description'),
            'image': data.get('image'),
            'seller': SellerOutWithInfoSerializer().to_internal_value(data.get('seller')),
            'items_available': data.get('items_available'),
            'tags': data.get('tags'),
        }
