from django.urls import path
from catalogue.views import products_list
urlpatterns = [
    path('product/list/', products_list, name='product-list')

]
