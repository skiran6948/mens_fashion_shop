from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('search/', views.search_products, name='search'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),


]
