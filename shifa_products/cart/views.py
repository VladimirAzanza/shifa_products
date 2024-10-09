from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import CartItemForm
from .mixins import (
    CartItemMixin, CartItemUpdateDeleteSuccessUrl, OnlyAuthorCartMixin
)
from .models import Cart, CartItem
from .constants import SUCCESFUL_ADD_T0_CART_MESSAGE
from catalog.models import Product


class AddToCartCreateView(LoginRequiredMixin, CreateView):
    model = CartItem
    form_class = CartItemForm
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
        messages.success(self.request, SUCCESFUL_ADD_T0_CART_MESSAGE)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.object.product.pk}
        )


class CartDetailView(OnlyAuthorCartMixin, DetailView):
    def get_object(self, queryset=None):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_item'] = self.get_object().cart_items.annotate(
            total_item=F('quantity') * F('product__price')
        )
        context['cart_total'] = self.get_object().cart_items.aggregate(
            cart_total=Sum(F('quantity') * F('product__price'), default=0)
        )['cart_total']
        context['addresses'] = self.request.user.addresses.all()
        return context


class CartItemUpdateView(
    CartItemMixin, CartItemUpdateDeleteSuccessUrl, UpdateView
):
    form_class = CartItemForm


class CartItemDeleteView(
    CartItemMixin, CartItemUpdateDeleteSuccessUrl, DeleteView
):
    pass
