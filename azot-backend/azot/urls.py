"""
URL configuration for azots project.

"""
from django.contrib import admin
from django.urls import path
from apps.views import (ClientRegisterView, ClientLoginView, SellerRegisterView, SellerLoginView,
                        SellerAddProductView, GetProductsView, ClientCartView, ClientAddBalanceView, ClientChangeInfoView,
                        SellerChangeInfoView, ClientBuyProductView, SellerProductView, ClientReviewSellerView, ClientReviewProductView,
                        SellerActivateView, ClientActivateView, ClientForgotPasswordView, SellerForgotPasswordView, password_reset,
                        SellerChangeInfoView, ClientBuyProductView, SellerProductView, ClientReviewSellerView, ClientReviewProductView, GetRandomProductsView,
                        SellerGetPurchasesView, ClientGetPurchasesView, UserChangePasswordView, GetProductByIdView)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seller/register', SellerRegisterView.as_view()),
    path('api/seller/login', SellerLoginView.as_view()),
    path('api/client/register', ClientRegisterView.as_view()),
    path('api/client/login', ClientLoginView.as_view()),
    path('api/seller/<str:seller_id>/product', SellerAddProductView.as_view()),
    path('api/product', GetProductsView.as_view()),
    path('api/client/<str:client_id>/cart', ClientCartView.as_view()),
    path('api/client/<str:client_id>/balance', ClientAddBalanceView.as_view()),
    path('api/client/<str:client_id>', ClientChangeInfoView.as_view()),
    path('api/seller/<str:seller_id>', SellerChangeInfoView.as_view()),
    path('api/client/<str:client_id>/product/<str:product_id>', ClientBuyProductView.as_view()),
    path('api/seller/<str:seller_id>/product/<str:product_id>', SellerProductView.as_view()),
    path('api/client/<str:client_id>/review/seller/<str:product_id>', ClientReviewSellerView.as_view()),
    path('api/client/<str:client_id>/review/product/<str:product_id>', ClientReviewProductView.as_view()),

    path('api/seller/activate/<str:token_id>', SellerActivateView.as_view()),
    path('api/client/activate/<str:token_id>', ClientActivateView.as_view()),
    path('api/password/client', ClientForgotPasswordView.as_view()),
    path('api/password/seller', SellerForgotPasswordView.as_view()),
    path('reset-password/', password_reset, name='password_reset'),

    path('api/product/random', GetRandomProductsView.as_view()),
    path('api/seller/<str:seller_id>/purchases', SellerGetPurchasesView.as_view()),
    path('api/client/<str:client_id>/purchases', ClientGetPurchasesView.as_view()),
    path('api/<str:user_id>/change_password', UserChangePasswordView.as_view()),
    path('api/product/id/<str:product_id>', GetProductByIdView.as_view()),
]
