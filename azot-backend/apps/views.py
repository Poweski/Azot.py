import uuid
from datetime import timedelta
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
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

from apps.mail_sender import sendmail

from apps.models import Client, Seller, Product, Purchase, Cart, Order, ProductReview, SellerReview, PasswordResetToken, \
    ActivationToken

from apps.exceptions import PurchaseError, PermissionDenied, NotActivated


class ClientRegisterView(APIView):
    def post(self, request):
        client = ClientInSerializer(data=request.data)
        client.is_valid(raise_exception=True)
        instance = client.create(client.validated_data)

        atoken = ActivationToken.objects.create(id=uuid.uuid4(),
                                                client=instance,
                                                expiration_date=timezone.now() + timedelta(minutes=60))

        subject = 'Activation of your client account in Azot'
        message = f'Hi {instance.email}, thank you for registering in Azot application. To activate your account, please click the link below:\n\nhttp://{settings.HOST_NAME}:{settings.APPLICATION_PORT}/api/client/activate/{atoken.id}'
        sendmail(subject, message, instance.email)

        return Response({'content': ClientOutSerializer(instance).data}, status=status.HTTP_200_OK)


class ClientActivateView(APIView):
    def get(self, request, token_id):
        atoken = ActivationToken.objects.get(id=token_id)
        if atoken.expiration_date < timezone.now():
            atoken.delete()
            raise NotAuthenticated()

        instance = atoken.client
        instance.isEnabled = True
        instance.save()

        atoken.delete()

        return Response("Your account has been successfully activated", status=status.HTTP_200_OK)


class ClientForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']

        instance = Client.objects.get(email=email)
        if not instance:
            raise NotAuthenticated()

        if not instance.isEnabled:
            raise PermissionDenied()

        prtoken = PasswordResetToken.objects.create(
            id=uuid.uuid4(),
            client=instance,
            expiration_date=timezone.now() + timedelta(minutes=60)
        )

        subject = 'Password recovery in Azot'
        message = f'Hi {instance.email}, to recover your password, please click the link below:\n\nhttp://{settings.HOST_NAME}:{settings.APPLICATION_PORT}/reset-password/?token={prtoken.id}&type=client'
        sendmail(subject, message, email)

        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class ClientLoginView(APIView):
    def post(self, request):
        client = ClientInSerializer(data=request.data)
        client.is_valid(raise_exception=True)
        instance = Client.objects.get(email=client.validated_data['email'])

        if instance.password == client.validated_data['password']:
            if not instance.isEnabled:
                raise PermissionDenied()
            else:
                return Response({'content': ClientOutWithInfoSerializer(instance).data}, status=status.HTTP_200_OK)
        else:
            raise NotAuthenticated()


class SellerRegisterView(APIView):
    def post(self, request):
        seller = SellerInSerializer(data=request.data)
        seller.is_valid(raise_exception=True)
        instance = seller.create(seller.validated_data)

        atoken = ActivationToken.objects.create(id=uuid.uuid4(),
                                                seller=instance,
                                                expiration_date=timezone.now() + timedelta(minutes=60))

        subject = 'Activation of your seller account in Azot'
        message = f'Hi {instance.email}, thank you for registering in Azot application. To activate your account, please click the link below:\n\nhttp://{settings.HOST_NAME}:{settings.APPLICATION_PORT}/api/seller/activate/{atoken.id}'
        sendmail(subject, message, instance.email)

        return Response({'content': SellerOutSerializer(instance).data}, status=status.HTTP_200_OK)


class SellerActivateView(APIView):
    def get(self, request, token_id):
        atoken = ActivationToken.objects.get(id=token_id)
        if atoken.expiration_date < timezone.now():
            atoken.delete()
            raise NotAuthenticated()

        instance = atoken.seller
        instance.isEnabled = True
        instance.save()

        atoken.delete()

        return Response("Your account has been successfully activated", status=status.HTTP_200_OK)


class SellerForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']

        instance = Seller.objects.get(email=email)
        if not instance:
            raise NotAuthenticated()

        if not instance.isEnabled:
            raise PermissionDenied()

        prtoken = PasswordResetToken.objects.create(
            id=uuid.uuid4(),
            seller=instance,
            expiration_date=timezone.now() + timedelta(minutes=60)
        )

        subject = 'Password recovery in Azot'
        message = f'Hi {instance.email}, to recover your password, please click the link below:\n\nhttp://{settings.HOST_NAME}:{settings.APPLICATION_PORT}/reset-password/?token={prtoken.id}&type=seller'
        sendmail(subject, message, email)

        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class SellerLoginView(APIView):
    def post(self, request):
        seller = SellerInSerializer(data=request.data)
        seller.is_valid(raise_exception=True)
        instance = Seller.objects.get(email=seller.validated_data['email'])
        if instance.password == seller.validated_data['password']:
            if not instance.isEnabled:
                raise PermissionDenied()
            else:
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


class ClientCartView(APIView):
    def put(self, request, client_id):
        client = Client.objects.get(id=client_id)
        orders = request.data['orders']
        cart = client.cart
        for order in orders:
            product = Product.objects.get(id=order['product'])
            Order.objects.create(id=uuid.uuid4(), product=product, quantity=order['quantity'], cart=cart)

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

            Purchase.objects.create(id=uuid.uuid4(), seller=order.product.owner, product_name=order.product.name,
                                    quantity=order.quantity, cost=order.product.price * order.quantity, client=client)

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
        if request.data['balance'] < 0:
            raise ValidationError()
        client.client_info.balance += request.data['balance']
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

        Purchase.objects.create(id=uuid.uuid4(), seller=product.owner, product_name=product.name, quantity=1,
                                cost=product.price, client=client)

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


def password_reset(request):
    if request.method == 'POST':
        token_id = request.POST.get('token')
        type = request.POST.get('type')
        prtoken = PasswordResetToken.objects.get(id=token_id)

        if prtoken.expiration_date < timezone.now():
            prtoken.delete()
            raise NotAuthenticated()

        password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            raise ValidationError()

        if not password:
            raise ValidationError()

        if type == 'client':
            instance = prtoken.client
        else:
            instance = prtoken.seller

        instance.password = password
        instance.save()

        prtoken.delete()

        return render(request, 'successful-reset.html')

    token = request.GET.get('token')
    type = request.GET.get('type')
    context = {
        'token': token,
        'type': type,
    }
    return render(request, 'reset-password.html', context)
