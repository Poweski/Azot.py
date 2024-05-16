from rest_framework import serializers

from apps.serializers.tojson.product_serializers import ProductOutSerializer

class OrderOutSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    product = ProductOutSerializer()

    def to_representation(self, instance):
        return {
            'quantity': instance.quantity,
            'product': ProductOutSerializer().to_representation(instance.product),
        }

    def to_internal_value(self, data):
        return {
            'quantity': data.get('quantity'),
            'product': ProductOutSerializer().to_internal_value(data.get('product')),
        }


class CartOutSerializer(serializers.ModelSerializer):
    orders = OrderOutSerializer(many=True)

    def to_representation(self, instance):
        return {
            'orders': [OrderOutSerializer().to_representation(order) for order in instance.orders.all()],
        }

    def to_internal_value(self, data):
        return {
            'orders': [OrderOutSerializer().to_internal_value(order) for order in data.get('orders')],
        }


