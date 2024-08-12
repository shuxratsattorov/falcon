from django.contrib import admin
from django.urls import path

from app.views import views, auth

urlpatterns = [
    # product
    path('', views.product_list, name='product_list'),
    path('product-detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product-commnet/<slug:slug>', views.comment, name='product_review'),

    # customers
    path('customers/', views.customers, name='customers'),
    path('customer-detail<int:id>', views.customer_detail, name='customer_detail'),

    # shopping card
    path('show-cart/', views.show_cart, name='show_cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('delete_cart_item/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('checkout/', views.checkout, name='checkout'),

    path('like/<slug:slug>/', views.like_product, name='like_product'),

    # auth
    path('accounts/login/', auth.login_page, name='login'),
    path('logout/', auth.logout_page, name='logout'),
    path('register/', auth.register_page, name='register'),
]

