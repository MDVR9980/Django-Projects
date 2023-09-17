from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Post


# from django.shortcuts import render


def post_list(request, year=None, month=None):
    if month is not None:
        return HttpResponse(f'Post list archive for {year} and {month}')

    if year is not None:
        return HttpResponse(f'Post list archive for {year}')
    return HttpResponse('Posts list page')


class BlogPostListView(ListView):
    model = Post


def categories_list(request):
    return HttpResponse('Category list page')


def post_detail(request, post_title):
    return HttpResponse(f'Post detail {post_title}')


class BlogPostDetailView(DetailView):
    model = Post


def custom_post_detail(request):
    return HttpResponse(f"Custom Post detail")


# def about(request):
#     return render(request, 'about.html')

