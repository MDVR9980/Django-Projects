from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
# from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, FormView

from shipping.forms import ShippingAddressForm
from shipping.models import ShippingAddress


# @login_required
# @require_GET
# def address_list(request):
#     # todo: Get all address for current user
#     # todo: pass to the right template
#     queryset = ShippingAddress.objects.filter(user=request.user)
#     return render(request, 'shipping/list.html', {'queryset': queryset})


class CustomUserListView(ListView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    # context_object_name = 'addresses'


class AddressListView(CustomUserListView):
    model = ShippingAddress
    # template_name = 'shipping/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_date'] = self.get_queryset().count()
        return context

    # @method_decorator(login_required)
    # def get(self, request):
    #     queryset = ShippingAddress.objects.filter(user=request.user)
    #     return render(request, 'shipping/list.html', {'queryset': queryset})

    # def post


# @login_required
# @require_http_methods(request_method_list=['GET', 'POST'])
# def address_create(request):
#     if request.method == "POST":
#         form = ShippingAddressForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             # instance.user = request.user
#             # instance.save()
#             return redirect('address-list')
#
#     else:
#         form = ShippingAddressForm()
#     return render(request, 'shipping/create.html', {'form': form})


class AddressCreateView(FormView):
    form_class = ShippingAddressForm
    template_name = 'shipping/create.html'
    # success_url = '/shipping/list/'
    success_url = reverse_lazy('address-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)
