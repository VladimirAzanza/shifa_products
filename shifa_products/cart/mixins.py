from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import Cart, CartItem


class OnlyAuthorCartMixin(UserPassesTestMixin):
    """Mixin to ensure that only the owner of a cart can access and modify it.

    Inherits from:
        - UserPassesTestMixin: Provides the 'test_func()' method to check
        access permissions.

    Methods:
        test_func():
            Verifies whether the current user is the owner of the cart or the
            cart item being accessed.
        handle_no_permission():
            Redirects to the product list if the user doesn't have permission
            to access the cart.
    """
    def test_func(self):
        object = self.get_object()
        if isinstance(object, Cart):
            return object.user == self.request.user
        else:
            return object.cart.user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('catalog:product_list'))


class CartItemUpdateDeleteSuccessUrl():
    """Mixin to provide the success URL for update/delete views of a cart item.

    Methods:
        get_success_url():
            Returns the URL to redirect to the cart after a successful
            operation.
    """
    def get_success_url(self):
        return reverse_lazy('cart:cart')


class CartItemMixin(OnlyAuthorCartMixin):
    """Mixin to handle operations related to cart items, restricting access to
    the owner only.

    Inherits from:
        - OnlyAuthorCartMixin: Ensures that only the cart owner can access and
        modify the items.

    Attributes:
        model (Model): The model associated with the view 'CartItem'.
        pk_url_kwarg (str): The name of the URL parameter used to identify a
        cart item.
    """
    model = CartItem
    pk_url_kwarg = 'cart_item_id'
