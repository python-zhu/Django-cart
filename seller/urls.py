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
from django.urls import path
from seller import views
urlpatterns = [
    path('login/', views.login),
    # path('register/', views.register),
    path('register/', views.register1),
    path('index/', views.index),
    path('logout/', views.logout),
    # path('type_add/', views.type_add),
    # path('type_add_ajax/', views.type_add_ajax),
    path('type_list/', views.type_list),
    path('type_change/', views.type_change),
    path('type_delete/', views.type_delete),
    path('type_add/', views.type_add1),
    path('type_add_ajax/', views.type_add_ajax1),
    path('register_ajax/', views.register_ajax),
    path('goods_add/', views.goods_add),
    path('goods_list/', views.goods_list),
    path('goods_delete/', views.goods_delete),
    path('goods_change/', views.goods_change),
    path('touxiang/', views.touxiang),
    path('xuanze/', views.xuanze),
]
