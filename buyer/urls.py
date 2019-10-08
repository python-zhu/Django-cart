"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from buyer import views

urlpatterns = [
    path('index/', views.index),
    path('goods_detail/', views.goods_detail),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('address_list/', views.address_list),
    path('address_add/', views.address_add),
    path('address_delete/', views.address_delete),
    path('address_update/', views.address_update),
    path('car_list/', views.car_list),
    path('car_jump/', views.car_jump),
    path('car_delete/', views.car_delete),
    path('car_goods_delete/', views.car_goods_delete),
    # path('enter_order/', views.enter_order),
    # path('alipay_method/', views.alipay_method),
    # path('register_email/', views.register_email),
    # path('send_message/', views.send_message),
]
