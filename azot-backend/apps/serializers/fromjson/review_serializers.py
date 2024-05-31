import uuid

from rest_framework import serializers
from apps.models import ProductReview, SellerReview


class ProductReviewInSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    text = serializers.CharField(allow_blank=True)

    def create(self, validated_data, *args, **kwargs):
        return ProductReview.objects.create(id=uuid.uuid4(),
                                            product=args[0],
                                            client=args[1],
                                            text=validated_data['text'],
                                            rating=validated_data['rating'])
    def update(self, instance, validated_data, *args, **kwargs):
        instance.text = validated_data.get('text', instance.text)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

class SellerReviewInSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    text = serializers.CharField(allow_blank=True)

    def create(self, validated_data, *args, **kwargs):
        return SellerReview.objects.create(id=uuid.uuid4(),
                                            seller=args[0],
                                            client=args[1],
                                            text=validated_data['text'],
                                            rating=validated_data['rating'])

    def update(self, instance, validated_data, *args, **kwargs):
        instance.text = validated_data.get('text', instance.text)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance
