from django import forms

from django.core.exceptions import ValidationError

# from lib.validators import min_length_validator
from shipping.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    # zipcode = forms.CharField(validators=[min_length_validator])

    class Meta:
        model = ShippingAddress
        fields = ('city', 'zipcode', 'address', 'number')
        # exclude = ('user',)
        # fields = '__all__' Bad

    def clean_zipcode(self):
        zipcode = self.cleaned_data['zipcode']
        # city = self.cleaned_data['city']
        if len(zipcode) != 16:
            raise ValidationError("length is not 16")

        return zipcode

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
