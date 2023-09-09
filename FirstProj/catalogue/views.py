from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

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

    products = Product.objects.select_related('category').all()
    context = "\n".join([f"{product.title}, {product.upc}, {product.category.name}" for product in products])
    return HttpResponse(context)


def product_detail(request, pk):
    # try:
    #     product = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     try:
    #         product = Product.objects.get(upc=pk)
    #     except Product.DoesNotExist:
    #         return HttpResponse("Product does not exist")  # use get!
    queryset = Product.objects.filter(is_active=True).filter(Q(pk=pk) | Q(upc=pk))
    if queryset.exists():
        product = queryset.first()
        return HttpResponse(f"title: {product.title}")
    return HttpResponse("Product does not exist")


def categury_products(request, pk):
    try:
        categury = Category.objects.prefetch_related('products').get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse("")
    products = categury.products.all()
    product_ids = [1, 2, 3]
    products = Product.objects.filter(id__in=product_ids)
    # products = Product.objects.filter(category=categury)

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
