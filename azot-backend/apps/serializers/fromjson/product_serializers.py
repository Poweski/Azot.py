import uuid

from rest_framework import serializers
from apps.models import Product


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