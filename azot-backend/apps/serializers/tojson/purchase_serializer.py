import uuid

from rest_framework import serializers
from apps.serializers.tojson.product_serializers import ProductOutSerializer

class PurchaseSerializer(serializers.ModelSerializer):
    product = ProductOutSerializer()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)


    def to_representation(self, instance):
        return {
            'product': ProductOutSerializer().to_representation(instance.product),
            'quantity': instance.quantity,
            'date': instance.date,
            'cost': instance.cost,
        }

    def to_internal_value(self, data):
        return {
            'product': ProductOutSerializer().to_internal_value(data.get('product')),
            'quantity': data.get('quantity'),
            'date': data.get('date'),
            'cost': data.get('cost'),
        }

