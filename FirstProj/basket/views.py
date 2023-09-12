from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_POST


@require_POST
def add_to_basket(request):
    # todo-1: check if user has basket_id cookie
    # todo-2: create and assign if doesn't have
    # todo-2-1: check if user is authenticated, set user to the basket
    # todo-3: get product from submitted form
    # todo-4: add product to the user basket lines
    # todo-5: return to the 'next' url
    # if request.cookie.get('basket_id', None):
    print("Request received")
    return HttpResponseRedirect('/catalogue/product/list/')


