from django.urls import path, register_converter
from blog.views import post_list, categories_list, post_detail
from blog.utils import FourDigitYear


register_converter(FourDigitYear, 'fourdigit')

urlpatterns = [
    path('list/', post_list),
    path('detail/<str:post_title>/', post_detail),
    path('categories/list/', categories_list),
    path('archive/<fourdigit:year>/', post_list),
    path('archive/<int:year>/<int:month>/', post_list),
]
