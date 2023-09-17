from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.shortcuts import render

from basket.forms import AddToBasketForm
from catalogue.models import Product, Category, Brand, ProductType
from catalogue.utils import check_is_active, check_is_staff


def products_list(request):

    # products = Product.objects.filter(is_active=True)
    # products = Product.objects.exclude(is_active=False)

    # category = Category.objects.first()
    # category = Category.objects.last()

    # category = Category.objects.get(id=1)
    # products = Product.objects.filter(is_active=True, category=category)
    # products = Product.objects.filter(is_active=True, category__id=1)

    # category = Category.objects.filters(name="Book").first()
    # products = Product.objects.filter(is_active=True, category__name="Book")
    #
    # brand = Brand.objects.first()
    # product_type = ProductType.objects.filter(title='Book')
    # new_product = Product.objects.create(
    #     product_type=product_type, upc=666, title="Test Product",
    #     description='', category=category, brand=brand
    # ),

    # Product.objects.filter(is_active=True, category=category).filter(brand=brand)

    context = dict()
    context['products'] = Product.objects.select_related('category').all()
    # context = "\n".join([f"{product.title}, {product.upc}, {product.category.name}" for product in products])
    # return HttpResponse(context)
    return render(request, 'catalogue/product_list.html', context=context)


def product_detail(request, pk):

    queryset = Product.objects.filter(is_active=True).filter(Q(pk=pk) | Q(upc=pk))
    if queryset.exists():
        product = queryset.first()
        form = AddToBasketForm({"product": product.id, 'quantity': 1})
        return render(request, 'catalogue/product_detail.html', {"product": product, "form": form})
    raise Http404


def category_products(request, pk):
    try:
        category = Category.objects.prefetch_related('products').get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse("")
    products = category.products.all()
    product_ids = [1, 2, 3]
    products = Product.objects.filter(id__in=product_ids)
    # products = Product.objects.filter(category=category)

    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(context)


def products_search(request):
    title = request.GET.get('q')

    products = Product.objects.actives(
        title__icontains=title,
        category__name__icontains=title, category__is_active=True
    )  # title__istartswith=title,
    # products = Product.objects.filter(is_active=True).filter(
    #     title__icontains=title
    # ).filter(category__name__icontains=title).filter(category__is_active=True).distinct()
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])

    return HttpResponse(f"Search page:\n{context}")


@login_required()
@require_http_methods(request_method_list=['GET', 'POST'])
# @require_GET
# @require_POST
@user_passes_test(check_is_active)
# @user_passes_test(check_is_staff)
@user_passes_test(lambda u: u.is_staff)
# @user_passes_test(lambda u: u.is_staff, login_url ='')
@permission_required('transaction.has_score_permission')
def user_profile(request):
    if check_is_active(request.user):
        return HttpResponse(f"Hello {request.user.username}")


@login_required()
# @require_GET
@require_POST
@user_passes_test(lambda u: u.score > 20)
@user_passes_test(lambda u: u.age > 14)
def campaign(request):
    pass
