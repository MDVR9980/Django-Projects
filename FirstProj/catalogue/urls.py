from django.urls import path
from catalogue.views import products_list, product_detail, categury_products, products_search, user_profile, campaign
urlpatterns = [
    path('product/list/', products_list, name='product-list'),
    path('product/search/', products_search, name='product-search'),
    path('product/detail/<int:pk>/', product_detail, name='product-detail'),
    path('categury/<int:pk>/products/', categury_products, name='categury-product'),
    path('profile/', user_profile, name='user-profile'),
    path('campaign/', campaign, name='campaign')
]
