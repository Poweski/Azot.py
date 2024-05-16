import uuid

from rest_framework import serializers
from apps.models import Product


class ProductInSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    image = serializers.URLField()
    items_available = serializers.IntegerField()
    tags = serializers.CharField()

    def create(self, validated_data, *args, **kwargs):
        return Product.objects.create(id=uuid.uuid4(),
                                      name=validated_data.get('name'),
                                      price=validated_data.get('price'),
                                      description=validated_data.get('description'),
                                      image=validated_data.get('image'),
                                      items_available=validated_data.get('items_available'),
                                      tags=validated_data.get('tags'),
                                      seller=args[0])

    def update(self, instance, validated_data, *args, **kwargs):
        instance.id = uuid.uuid4()
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.items_available = validated_data.get('items_available', instance.items_available)
        instance.tags = validated_data.get('tags', instance.tags)
        seller = args[0]
        instance.seller = seller
        instance.save()
        return instance