from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Cart, CartItem


class OnlyAuthorCartMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        if isinstance(object, Cart):
            return object.user == self.request.user
        else:
            return object.cart.user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('catalog:product_list'))


class CartItemUpdateDeleteSuccessUrl():
    def get_success_url(self):
        return reverse_lazy('cart:cart')


class CartItemMixin(OnlyAuthorCartMixin):
    model = CartItem
    pk_url_kwarg = 'cart_item_id'
