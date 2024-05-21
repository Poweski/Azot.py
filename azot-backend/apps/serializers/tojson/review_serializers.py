from rest_framework import serializers
import apps.serializers.tojson.client_serializers


class ProductReviewOutSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    rating = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'text': instance.text,
            'rating': instance.rating,
            'client': apps.serializers.tojson.client_serializers.ClientOutShortSerializer().to_representation(instance.client),
        }

class SellerReviewOutSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    rating = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'text': instance.text,
            'rating': instance.rating,
            'client': apps.serializers.tojson.client_serializers.ClientOutShortSerializer().to_representation(instance.client),
        }
