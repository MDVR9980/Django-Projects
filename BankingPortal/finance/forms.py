from django import forms


class ChargeWalletForm(forms.Form):
    amount = forms.IntegerField()
