"""
URL configuration for barbershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views
from .views import create_review, get_master_info



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('thanks/', views.thanks, name='thanks'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("services/create/", views.service_create, name="service_create"),
    path('reviews/create/', create_review, name='create_review'),
    path('api/master-info/', get_master_info, name='get_master_info'),
]