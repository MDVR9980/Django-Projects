from django.http import HttpResponseRedirect, Http404
from django.views.decorators.http import require_POST
from basket.forms import AddToBasketForm
from basket.models import Basket
from catalogue.models import Product


@require_POST
def add_to_basket(request):
    # todo-1: check if user has basket_id cookie
    # todo-2: create and assign if doesn't have
    # todo-2-1: check if user is authenticated, set user to the basket
    # todo-3: get product from submitted form
    # todo-4: add product to the user basket lines
    # todo-5: return to the 'next' url

    # With Django Form Builder:
    response = HttpResponseRedirect(request.POST.get('next', '/'))

    basket = Basket.get_basket(request.COOKIES.get('basket_id', None))
    if basket is None:
        raise Http404

    response.set_cookie('basket_id', basket.id)

    if not basket.validate_user(request.user):
        raise Http404

    form = AddToBasketForm(request.POST)
    if form.is_valid():
        form.save(basket=basket)

    return response
    #     basket = Basket.objects.create()
    #     response.set_cookie('basket_id', basket.id)
    # else:
    #     try:
    #         basket = Basket.objects.get(pk=basket_id)
    #     except Basket.DoesNotExist:
    #         raise Http404
    #
    # if not basket.validate_user(request.user):
    #     raise Http404

    # if request.user.is_authenticated:
    #     if basket.user is not None and basket.user != request.user:
    #         raise Http404
    #     basket.user = request.user
    #     basket.save()

    # ٔNo Django Form Builder:
    # response = HttpResponseRedirect(request.POST.get('next', '/'))
    #
    # basket_id = request.COOKIES.get('basket_id', None)
    # if basket_id is None:
    #     basket = Basket.objects.create()
    #     response.set_cookie('basket_id', basket.id)
    # else:
    #     try:
    #         basket = Basket.objects.get(pk=basket_id)
    #     except Basket.DoesNotExist:
    #         raise Http404
    #
    # if request.user.is_authenticated:
    #     if basket.user is not None and basket.user != request.user:
    #         raise Http404
    #     basket.user = request.user
    #     basket.save()
    #
    # product_id = request.POST.get('product_id', None)
    # quantity = request.POST.get('quantity', 1)
    # try:
    #     quantity = int(quantity)
    # except:
    #     quantity = 1
    # if product_id is not None:
    #     try:
    #         product = Product.objects.get(pk=product_id)
    #     except Product.DoesNotExist:
    #         raise Http404
    #     else:
    #         basket.add(product, quantity)
    # return response
