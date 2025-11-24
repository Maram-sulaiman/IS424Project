from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('products/', views.products_view, name='products'),
    path('product/<int:id>/', views.product_details, name='product_details')
]