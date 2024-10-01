from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AddToCartForm
from .models import Cart, CartItem
from catalog.models import Product


class AddToCartCreateView(LoginRequiredMixin, CreateView):
    model = CartItem
    form_class = AddToCartForm
    pk_url_kwarg = 'product_id'
    product = None
    cart = None

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            Product,
            pk=self.kwargs.get(self.pk_url_kwarg)
        )
        self.cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.product
        form.instance.cart = self.cart
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.object.product.pk}
        )
