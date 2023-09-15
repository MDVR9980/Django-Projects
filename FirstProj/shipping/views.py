from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from shipping.forms import ShippingAddressForm


def address_list(request):
    return HttpResponse("Address list")


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def address_create(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('address-list')

    else:
        form = ShippingAddressForm()
    return render(request, 'shipping/create.html', {'form': form})
