from django.db import models


class IsActiveManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related('category', 'brand')

    def actives(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(as_active=True)


class IsActiveCategoryManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(category__is_active=True)


class ProductType(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    modifies_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ProductType"
        verbose_name_plural = "ProductTypes"
        # db_table = '...' اسمی که مد نظرمون هستش که خودمون ست کنیم برای تیبل

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    INTEGER = 1
    STRING = 2
    FLOAT = 3

    ATTRIBUTE_TYPES_FIELDS = (
        (INTEGER, "Integer"),
        (STRING, "String"),
        (FLOAT, "Float"),
    )
    title = models.CharField(max_length=32)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='attributes')
    attribute_type = models.PositiveSmallIntegerField(default=INTEGER, choices=ATTRIBUTE_TYPES_FIELDS)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('category-detail', args=[self.pk])


class Brand(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products_types', null=True)
    upc = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')

    default_manager = models.Manager()
    objects = IsActiveManager()
    is_active_category_manager = IsActiveCategoryManager()

    def __str__(self):
        return self.title

    @property
    def stock(self):
        return self.partners.all().order_by('price').first()


class ProductImage(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.product)


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    value = models.CharField(max_length=48)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT, related_name='values')

    def __str__(self):
        return f"{self.product}({self.attribute}): {self.value}"
