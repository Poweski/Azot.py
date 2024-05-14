"""
URL configuration for azots project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.views import (ClientRegisterView, ClientLoginView, SellerRegisterView, SellerLoginView,
                        SellerAddProductView, GetProductsView, ClientBuyProductView, ClientAddBalanceView, ClientChangeInfoView,
                        SellerChangeInfoView)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/seller/register', SellerRegisterView.as_view()),
    path('api/seller/login', SellerLoginView.as_view()),
    path('api/client/register', ClientRegisterView.as_view()),
    path('api/client/login', ClientLoginView.as_view()),
    path('api/seller/<str:seller_id>/product', SellerAddProductView.as_view()),
    path('api/product', GetProductsView.as_view()),
    path('api/client/<str:client_id>/product/<str:product_id>', ClientBuyProductView.as_view()),
    path('api/client/<str:client_id>/balance', ClientAddBalanceView.as_view()),
    path('api/client/<str:client_id>', ClientChangeInfoView.as_view()),
    path('api/seller/<str:seller_id>', SellerChangeInfoView.as_view()),
]
