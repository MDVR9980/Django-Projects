from django.http import HttpResponse
# from django.shortcuts import render


def post_list(request, year=None, month=None):
    if month is not None:
        return HttpResponse(f'Post list archive for {year} and {month}')

    if year is not None:
        return HttpResponse(f'Post list archive for {year}')
    return HttpResponse('Posts list page')


def categories_list(request):
    return HttpResponse('Category list page')


def post_detail(request, post_title):
    return HttpResponse(f'Post detail {post_title}')


def custom_post_detail(request):
    return HttpResponse(f"Custom Post detail")