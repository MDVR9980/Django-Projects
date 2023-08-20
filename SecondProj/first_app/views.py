from django.shortcuts import render
from django.http import HttpResponse


def signup_view(request):
    return HttpResponse('Signup Completed!')
