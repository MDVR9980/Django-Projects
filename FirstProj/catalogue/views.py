from django.db.models import Q
from django.http import HttpResponse
from catalogue.models import Product, Category, Brand, ProductType


def products_list(request):
    products = Product.objects.all()

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

    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
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

