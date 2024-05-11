from django.core import serializers
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.serializers import (ClientInSerializer, ClientOutSerializer, SellerInSerializer, SellerOutSerializer,
                              ProductInSerializer, ProductOutSerializer, SellerInfoInSerializer, SellerInfoOutSerializer,
                              ClientInfoInSerializer, ClientInfoOutSerializer, SellerOutWithInfoSerializer, ClientOutWithInfoSerializer)

from apps.models import Client, Seller, Product

from apps.exceptions import PurchaseError


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
            return Response({'content': ClientOutSerializer(instance).data}, status=status.HTTP_200_OK)
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
            return Response({'content': SellerOutSerializer(instance).data}, status=status.HTTP_200_OK)
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

class ClientBuyProductView(APIView):
    def post(self, request, client_id, product_id):
        client = Client.objects.get(id=client_id)
        product = Product.objects.get(id=product_id)
        if client.client_info.balance < product.price:
            raise PurchaseError()
        client.client_info.balance -= product.price
        client.client_info.save()
        product.delete()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class ClientChangeInfoView(APIView):
    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        client_info = ClientInfoInSerializer(data=request.data)
        client_info.is_valid(raise_exception=True)
        client.client_info = client_info.update(client.client_info, client_info.validated_data)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        return Response({'content': ClientOutWithInfoSerializer(client).data}, status=status.HTTP_200_OK)

class SellerChangeInfoView(APIView):
    def post(self, request, seller_id):
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
        if request.data['balance'] < 0:
            raise ValidationError()
        client.client_info.balance += request.data['balance']
        client.client_info.save()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)


