from django.db import models
from django.contrib.auth.models import User
from catalogue.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='baskets', null=True, blank=True
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lines')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.basket} => {self.product}, {self.quantity}"
