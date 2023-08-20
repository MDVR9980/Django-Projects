from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    CHARGE = 1
    PURCHASE = 2
    TRANSFER = 3

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, "Charge"),
        (PURCHASE, "Purchase"),
        (TRANSFER, "Transfer"),
    )

    user = models.ForeignKey(User, related_name='transactions', on_delete=models.RESTRICT)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE_CHOICES, default=CHARGE)
    amount = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.get_transaction_type_display()} - {self.amount}"
