from django.db import models
from catalogue.models import Product


class Partner(models.Model):
    name = models.CharField(max_length=48)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class PartnerStock(models.Model):
    partner = models.ForeignKey(Partner, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='partners', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)

    def __Str__(self):
        return f"{self.partner} -> {self.product} : {self.price}"
