from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models import Q


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

    @classmethod
    def get_report(cls):
        """show all users and their balance"""
        positive_transactions = Sum(
            'transactions_amount',
            filter=Q(transactions__transaction_type=1)
        )
        negative_transactions = Sum(
            'transactions_amount',
            filter=Q(transactions__transaction_type__in=[2, 3])
        )
        users = User.objects.all().annotate(
            transactions_count=Count('transactions__id'),
            balance=Coalesce(positive_transactions, 0) - Coalesce(negative_transactions, 0)
        )
        return users

    @classmethod
    def get_total_balance(cls, user):
        queryset = cls.get_report()
        return queryset.aggregate(Sum('balance'))


class UserBalance(models.Model):
    user = models.ForeignKey(User, related_name='balance_records', on_delete=models.RESTRICT)
    balance = models.BigIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __sre__(self):
        return f"{self.user} - {self.balance} - {self.created_time}"
