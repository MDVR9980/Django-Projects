from django import forms

from shipping.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('city', 'zipCode', 'address', 'number')
        # exclude = ('user',)
        # fields = '__all__' Bad
