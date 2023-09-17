from django.urls import path, register_converter, re_path
from blog.views import post_list, categories_list, post_detail
from blog.utils import FourDigitYear


register_converter(FourDigitYear, 'fourdigit')

urlpatterns = [
    path('list/', post_list),
    path('detail/<int:pk>/', post_detail),
    path('detail/<str:post_title>/', post_detail),
    path('categories/list/', categories_list),
    path('archive/<fourdigit:year>/', post_list),
    path('archive/<int:year>/<int:month>/', post_list),
    re_path(r'archive/(?P<code>[0-9]{4})/', post_list),
    re_path(r'archive/(?P<code>[0-9]{6})/', post_list),

]
