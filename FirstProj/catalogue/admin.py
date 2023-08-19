from django.contrib import admin
from catalogue.models import Category, Brand, Product, ProductType


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_type', 'upc', 'title', 'category', 'brand']


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)
