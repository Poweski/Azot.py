import uuid

from rest_framework import serializers
from apps.models import Order, Cart


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.UUIDField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        return Order.objects.create(id=uuid.uuid4(),
                                    product=validated_data.get('product'),
                                    quantity=validated_data.get('quantity'))


# class ClientCartSerializer(serializers.ModelSerializer):
#      # orders = OrderSerializer()
#     #
#     # def update(self, instance, validated_data, *args, **kwargs):
#     #     validated_data.get('orders')
#     #     instance.save()
#     #     return instance

