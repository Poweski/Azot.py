from rest_framework import serializers

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
            'seller_info': SellerInfoShortOutSerializer().to_representation(instance.seller_info),
        }

    def to_internal_value(self, data):
        return {
            'seller_info': SellerInfoShortOutSerializer().to_internal_value(data.get('seller_info')),
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
        }

    def to_internal_value(self, data):
        return {
            'id': data.get('id'),
            'name': data.get('name'),
            'price': data.get('price'),
            'description': data.get('description'),
            'image': data.get('image'),
            'owner': SellerShortOutSerializer().to_internal_value(data.get('owner')),
            'items_available': data.get('items_available'),
            'tags': data.get('tags'),
        }

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




class SellerOutWithInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    seller_info = SellerInfoOutSerializer()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'seller_info': SellerInfoOutSerializer().to_representation(instance.seller_info),
            'products': ProductOutSerializer(instance.product_set.all(), many=True).data,
            'purchases': PurchaseSerializer(instance.purchase_set.all(), many=True).data,
        }



