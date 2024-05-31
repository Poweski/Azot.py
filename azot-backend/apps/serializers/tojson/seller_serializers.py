from django.db import models
from rest_framework import serializers
import apps.serializers.tojson.review_serializers


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

class SellerInfoShortOutSerializer(serializers.Serializer):
    organization = serializers.CharField()

    def to_representation(self, instance):
        return {
            'organization': instance.organization,
        }

    def to_internal_value(self, data):
        return {
            'organization': data.get('organization'),
        }

class SellerShortOutSerializer(serializers.Serializer):
    seller_info = SellerInfoShortOutSerializer()

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'seller_info': SellerInfoShortOutSerializer().to_representation(instance.seller_info),
            'average_rating': instance.sellerreview_set.all().aggregate(models.Avg('rating'))['rating__avg'],
            'reviews': apps.serializers.tojson.review_serializers.SellerReviewOutSerializer(instance.sellerreview_set.all(), many=True).data,
        }

class ProductOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    image = serializers.URLField()
    owner = SellerShortOutSerializer()
    items_available = serializers.IntegerField()
    tags = serializers.CharField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'price': instance.price,
            'description': instance.description,
            'image': instance.image,
            'owner': SellerShortOutSerializer().to_representation(instance.owner),
            'items_available': instance.items_available,
            'tags': instance.tags,
            'average_rating': instance.productreview_set.all().aggregate(models.Avg('rating'))['rating__avg'],
            'reviews': apps.serializers.tojson.review_serializers.ProductReviewOutSerializer(instance.productreview_set.all(), many=True).data,
        }

class ProductShortOutSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
        }


class PurchaseSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)


    def to_representation(self, instance):
        return {
            'product': instance.product_name,
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




class SellerOutWithInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    seller_info = SellerInfoOutSerializer()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'seller_info': SellerInfoOutSerializer().to_representation(instance.seller_info),
        }



