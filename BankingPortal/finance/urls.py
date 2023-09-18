from django.urls import path

from finance.views import ChargeWalletView

urlpatterns = [
    path('charge/', ChargeWalletView.as_view(), ),
]
