from rest_framework import serializers

from apps.serializers.tojson.seller_serializers import ProductOutSerializer

class OrderOutSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    product = ProductOutSerializer()

    def to_representation(self, instance):
        return {
            'quantity': instance.quantity,
            'product': ProductOutSerializer().to_representation(instance.product),
        }


class CartOutSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return {
            'orders': OrderOutSerializer(instance.order_set.all(), many=True).data,
        }


