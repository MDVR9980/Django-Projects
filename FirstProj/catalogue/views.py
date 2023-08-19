from django.http import HttpResponse
from django.shortcuts import render


def products_list(request):
    return HttpResponse('products lists')
