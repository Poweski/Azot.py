import uuid
from decimal import Decimal
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
from apps.serializers.tojson.seller_serializers import SellerOutSerializer, SellerOutWithInfoSerializer, ProductShortOutSerializer, PurchaseSerializer
from apps.serializers.fromjson.seller_serializers import SellerInSerializer, SellerInfoInSerializer
from apps.serializers.fromjson.review_serializers import ProductReviewInSerializer, SellerReviewInSerializer
from apps.serializers.tojson.client_cart_serializer import CartOutSerializer

from apps.utils.password_validator import validate_password


from apps.mail_sender import sendmail

from apps.models import Client, Seller, Product, Purchase, Cart, Order, ProductReview, SellerReview, PasswordResetToken, ActivationToken

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
            raise PermissionDenied("Wrong email or password")


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
            raise PermissionDenied("Wrong email or password")


class SellerAddProductView(APIView):
    def get(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        return Response({'content': ProductOutSerializer(seller.product_set.all(), many=True).data}, status=status.HTTP_200_OK)

    def post(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        product = ProductInSerializer(data=request.data)
        product.is_valid(raise_exception=True)
        new_product = product.create(product.validated_data, seller)
        return Response({'content': ProductShortOutSerializer(new_product).data}, status=status.HTTP_200_OK)


class GetProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        return Response({'content': ProductOutSerializer(products, many=True).data}, status=status.HTTP_200_OK)

    def post(self, request):
        request_text = request.data['request']
        tag_products = Product.objects.filter(tags__contains=request_text)
        name_products = Product.objects.filter(name__contains=request_text)
        products = tag_products | name_products
        return Response({'content': ProductOutSerializer(products, many=True).data}, status=status.HTTP_200_OK)

class GetRandomProductsView(APIView):
    def get(self, request):
        product = Product.objects.order_by('?')[0]
        return Response({'content': ProductOutSerializer(product).data}, status=status.HTTP_200_OK)

class GetProductByIdView(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return Response({'content': ProductOutSerializer(product).data}, status=status.HTTP_200_OK)

class ClientCartView(APIView):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        return Response({'content': CartOutSerializer(client.cart).data}, status=status.HTTP_200_OK)

    def put(self, request, client_id):
        client = Client.objects.get(id=client_id)
        orders = request.data['orders']
        cart = client.cart

        for order in cart.order_set.all():
            order.delete()

        for order in orders:
            product = Product.objects.get(id=order['product'])
            Order.objects.create(id=uuid.uuid4(), product=product, quantity=order['quantity'], cart = cart)

        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def post(self, request, client_id):
        client = Client.objects.get(id=client_id)
        cart = client.cart
        for order in cart.order_set.all():
            if client.client_info.balance < order.product.price * order.quantity:
                raise PurchaseError("Not enough money")
            if order.product.items_available < order.quantity:
                raise PurchaseError("Not enough items available")

            client.client_info.balance -= order.product.price * order.quantity
            client.client_info.save()

            order.product.items_available -= order.quantity
            order.product.save()

            Purchase.objects.create(id=uuid.uuid4(), seller=order.product.owner, product_name=order.product.name, quantity=order.quantity, cost=order.product.price * order.quantity, client=client, product_id=order.product.id)

            order.delete()

        return Response({'content': 'success'}, status=status.HTTP_200_OK)

class ClientGetPurchasesView(APIView):
    def get(self, request, client_id):
        client = Client.objects.get(id=client_id)
        purchases = client.purchase_set.all()
        return Response({'content': PurchaseSerializer(purchases, many=True).data}, status=status.HTTP_200_OK)

class SellerGetPurchasesView(APIView):
    def get(self, request, seller_id):
        seller = Seller.objects.get(id=seller_id)
        purchases = seller.purchase_set.all()
        return Response({'content': PurchaseSerializer(purchases, many=True).data}, status=status.HTTP_200_OK)

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
            raise PermissionDenied("Balance must be positive")

        client.client_info.balance += added_balance
        client.client_info.save()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class SellerProductView(APIView):
    def put(self, request, seller_id, product_id):
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.get(id=product_id)

        if product.owner != seller:
            raise PermissionDenied("You are not the owner of this product")

        product_serializer = ProductInSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.update(product, product_serializer.validated_data, seller)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)

    def delete(self, request, seller_id, product_id):
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.get(id=product_id)

        if product.owner != seller:
            raise PermissionDenied("You are not the owner of this product")

        product.delete()
        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class ClientBuyProductView(APIView):
    def post(self, request, client_id, product_id):
        client = Client.objects.get(id=client_id)
        product = Product.objects.get(id=product_id)
        if client.client_info.balance < product.price:
            raise PurchaseError("Not enough money")
        if product.items_available < 1:
            raise PurchaseError("Not enough items available")
        client.client_info.balance -= product.price
        client.client_info.save()

        product.items_available -= 1
        product.save()

        Purchase.objects.create(id=uuid.uuid4(), seller=product.owner, product_name=product.name, quantity=1, cost=product.price, client=client, product_id=product.id)

        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class ClientReviewProductView(APIView):
    def post(self, request, client_id, product_id):
        client = Client.objects.get(id=client_id)
        product = Product.objects.get(id=product_id)

        if not Purchase.objects.filter(product_name=product.name, client=client).first():
            raise PermissionDenied("You have not bought this product")

        if ProductReview.objects.filter(product=product, client=client).first():
            raise PermissionDenied("You have already reviewed this product")

        product_review = ProductReviewInSerializer(data=request.data)
        product_review.is_valid(raise_exception=True)
        product_review.create(product_review.validated_data, product, client)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class ClientReviewSellerView(APIView):
    def post(self, request, client_id, product_id):
        client = Client.objects.get(id=client_id)
        seller = Product.objects.get(id=product_id).owner

        if not Purchase.objects.filter(seller=seller, client=client).first():
            raise PermissionDenied("You have not bought from this seller")

        if SellerReview.objects.filter(seller=seller, client=client).first():
            raise PermissionDenied("You have already reviewed this seller")

        seller_review = SellerReviewInSerializer(data=request.data)
        seller_review.is_valid(raise_exception=True)
        seller_review.create(seller_review.validated_data, seller, client)
        return Response({'content': 'success'}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    def post(self, request, user_id):
        if request.data['type'] == 'client':
            user = Client.objects.get(id=user_id)
        elif request.data['type'] == 'seller':
            user = Seller.objects.get(id=user_id)
        else:
            raise PermissionDenied("Invalid user type")

        password = request.data['password']
        validate_password(password)

        user.password = password
        user.save()
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
