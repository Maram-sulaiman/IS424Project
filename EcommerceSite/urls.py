from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('products/', views.products_view, name='products'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path("basket/", views.basket_page, name="basket"),
    path("basket/add/<int:product_id>/", views.add_to_basket, name="add_to_basket"),
    path("basket/update/<int:product_id>/", views.update_quantity, name="update_quantity"),
    path("basket/remove/<int:product_id>/", views.remove_item, name="remove_item"),
    path("basket/clear/", views.clear_basket, name="clear_basket"),
    path("order/", views.order_page, name="order"),


    
]