from django.urls import path
from shipping.views import address_list, address_create
urlpatterns = [
    path('list/', address_list, name='address-list'),
    path('create/', address_create, name='address-create')
]
