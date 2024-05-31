import uuid
from decimal import Decimal
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.serializers.tojson.client_serializers import ClientOutSerializer, ClientOutWithInfoSerializer
from apps.serializers.tojson.seller_serializers import ProductOutSerializer
from apps.serializers.fromjson.product_serializers import ProductInSerializer
from apps.serializers.fromjson.client_serializers import ClientInSerializer, ClientInfoInSerializer
from apps.serializers.tojson.seller_serializers import SellerOutSerializer, SellerOutWithInfoSerializer
from apps.serializers.fromjson.seller_serializers import SellerInSerializer, SellerInfoInSerializer
from apps.serializers.fromjson.review_serializers import ProductReviewInSerializer, SellerReviewInSerializer





from apps.models import Client, Seller, Product, Purchase, Cart, Order, ProductReview, SellerReview

from apps.exceptions import PurchaseError, PermissionDenied



class ClientRegisterView(APIView):
    def post(self, request):
        client = ClientInSerializer(data=request.data)
        client.is_valid(raise_exception=True)
        instance = client.create(client.validated_data)
        return Response({'content': ClientOutSerializer(instance).data}, status=status.HTTP_200_OK)


class ClientLoginView(APIView):
    def post(self, request):
        client = ClientInSerializer(data=request.data)
        client.is_valid(raise_exception=True)
        instance = Client.objects.get(email=client.validated_data['email'])
        if instance.password == client.validated_data['password']:
            return Response({'content': ClientOutWithInfoSerializer(instance).data}, status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated()

class SellerRegisterView(APIView):
    def post(self, request):
        seller = SellerInSerializer(data=request.data)
        seller.is_valid(raise_exception=True)
        instance = seller.create(seller.validated_data)
        return Response({'content': SellerOutSerializer(instance).data}, status=status.HTTP_200_OK)


class SellerLoginView(APIView):
    def post(self, request):
        seller = SellerInSerializer(data=request.data)
        seller.is_valid(raise_exception=True)
        instance = Seller.objects.get(email=seller.validated_data['email'])
        if instance.password == seller.validated_data['password']:
            return Response({'content': SellerOutWithInfoSerializer(instance).data}, status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated()


class SellerAddProductView(APIView):
    def post(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        product = ProductInSerializer(data=request.data)
        product.is_valid(raise_exception=True)
        product.create(product.validated_data, seller)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class GetProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        return Response({'content': ProductOutSerializer(products, many=True).data}, status=status.HTTP_200_OK)


class GetRandomProductsView(APIView):
    def get(self, request):
        product = Product.objects.order_by('?')[0]
        return Response({'content': ProductOutSerializer(product).data}, status=status.HTTP_200_OK)


class ClientCartView(APIView):
    def put(self, request, client_id):
        client = Client.objects.get(id=client_id)
        orders = request.data['orders']
        cart = client.cart
        for order in orders:
            product = Product.objects.get(id=order['product'])
            Order.objects.create(id=uuid.uuid4(), product=product, quantity=order['quantity'], cart = cart)

        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        cart = client.cart
        for order in cart.order_set.all():
            if client.client_info.balance < order.product.price * order.quantity:
                raise PurchaseError()
            if order.product.items_available < order.quantity:
                raise PurchaseError()

            client.client_info.balance -= order.product.price * order.quantity
            client.client_info.save()

            order.product.items_available -= order.quantity
            order.product.save()

            Purchase.objects.create(id=uuid.uuid4(), seller=order.product.owner, product_name=order.product.name, quantity=order.quantity, cost=order.product.price * order.quantity, client=client)

            order.delete()


        return Response({'content': 'success'}, status=status.HTTP_200_OK)



class ClientChangeInfoView(APIView):
    def put(self, request, client_id):
        client = Client.objects.get(id=client_id)
        client_info = ClientInfoInSerializer(data=request.data)
        client_info.is_valid(raise_exception=True)
        client.client_info = client_info.update(client.client_info, client_info.validated_data)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        return Response({'content': ClientOutWithInfoSerializer(client).data}, status=status.HTTP_200_OK)

class SellerChangeInfoView(APIView):
    def put(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        seller_info = SellerInfoInSerializer(data=request.data)
        seller_info.is_valid(raise_exception=True)
        seller.seller_info = seller_info.update(seller.seller_info, seller_info.validated_data)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def get(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        return Response({'content': SellerOutWithInfoSerializer(seller).data}, status=status.HTTP_200_OK)


class ClientAddBalanceView(APIView):
    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        added_balance = Decimal(request.data['balance'])
        if added_balance < 0:
            raise ValidationError()

        client.client_info.balance += added_balance
        client.client_info.save()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class SellerProductView(APIView):
    def put(self, request, seller_id, product_id):
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.get(id=product_id)

        if product.owner != seller:
            raise PermissionDenied()

        product_serializer = ProductInSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.update(product, product_serializer.validated_data, seller)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def delete(self, request, seller_id, product_id):
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.get(id=product_id)

        if product.owner != seller:
            raise PermissionDenied()

        product.delete()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class ClientBuyProductView(APIView):
    def post(self, request, client_id, product_id):
        client = Client.objects.get(id=client_id)
        product = Product.objects.get(id=product_id)
        if client.client_info.balance < product.price:
            raise PurchaseError()
        if product.items_available < 1:
            raise PurchaseError()
        client.client_info.balance -= product.price
        client.client_info.save()

        product.items_available -= 1
        product.save()

        Purchase.objects.create(id=uuid.uuid4(), seller=product.owner, product_name=product.name, quantity=1, cost=product.price, client=client)

        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class ClientReviewProductView(APIView):
    def post(self, request, client_id, product_id):
        client = Client.objects.get(id=client_id)
        product = Product.objects.get(id=product_id)

        if not Purchase.objects.filter(product_name=product.name, client=client).first():
            raise PermissionDenied()

        if ProductReview.objects.filter(product=product, client=client).first():
            raise PermissionDenied()

        product_review = ProductReviewInSerializer(data=request.data)
        product_review.is_valid(raise_exception=True)
        product_review.create(product_review.validated_data, product, client)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class ClientReviewSellerView(APIView):
    def post(self, request, client_id, seller_id):
        client = Client.objects.get(id=client_id)
        seller = Seller.objects.get(id=seller_id)

        if not Purchase.objects.filter(seller=seller, client=client).first():
            raise PermissionDenied()

        if SellerReview.objects.filter(seller=seller, client=client).first():
            raise PermissionDenied()

        seller_review = SellerReviewInSerializer(data=request.data)
        seller_review.is_valid(raise_exception=True)
        seller_review.create(seller_review.validated_data, seller, client)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)


