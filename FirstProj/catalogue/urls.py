from django.urls import path
from catalogue.views import products_list, product_detail, categury_products
urlpatterns = [
    path('product/list/', products_list, name='product-list'),
    path('product/detail/<int:pk>/', product_detail, name='product-detail'),
    path('categury/<int:pk>/products/', categury_products, name='categury-product'),
]
