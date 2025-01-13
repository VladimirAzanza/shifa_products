from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import CartItemForm
from .mixins import (
    CartItemMixin, CartItemUpdateDeleteSuccessUrl, OnlyAuthorCartMixin
)
from .models import Cart, CartItem
from catalog.models import Product
from shifa_products.constants import (
    SUCCESFUL_ADD_T0_CART_MESSAGE, SIGN_IN_TO_ADD_CART_MESSAGE
)


class AddToCartCreateView(LoginRequiredMixin, CreateView):
    """View for adding a product to the cart.

    Inherits:
        - LoginRequiredMixin: Ensures the user is authenticated.
        - CreateView: Handles the creation of a new `CartItem`.

    Attributes:
        model (Model): The model for the view 'CartItem'.
        form_class (Form): The form for creating 'CartItem'.
        pk_url_kwarg (str): The URL keyword for the product 'product_id'.
        product (Product): The product to be added to the cart.
        cart (Cart): The cart for the logged-in user.

    Methods:
        dispatch(request, *args, **kwargs):
            Handles authentication and initializes the cart/product.
        form_valid(form):
            Assigns the product and cart to the `CartItem`.
        get_success_url():
            Returns the URL for redirection after success.
    """
    model = CartItem
    form_class = CartItemForm
    pk_url_kwarg = 'product_id'
    product = None
    cart = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, SIGN_IN_TO_ADD_CART_MESSAGE)
            return redirect('login')
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
            'catalog:category_product_list',
            kwargs={'category_slug': self.object.product.category.slug}
        )


class CartDetailView(OnlyAuthorCartMixin, DetailView):
    """View for displaying the details of the user's cart.

    Inherits from:
        - OnlyAuthorCartMixin: Restricts access to the cart owner.
        - DetailView: Displays the details of a single cart.

    Methods:
        get_object(queryset=None):
            Fetches or creates the cart for the logged-in user.

        get_context_data(**kwargs):
            Adds additional context to the template, such as cart items,
            total cost, and user addresses.
    """
    def get_object(self, queryset=None):
        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_object().cart_items.select_related(
            'product'
        ).annotate(total_item=F('quantity') * F('product__price'))
        context['cart_item'] = cart_items
        context['cart_total'] = cart_items.aggregate(
            cart_total=Sum(F('quantity') * F('product__price'), default=0)
        )['cart_total']
        context['addresses'] = self.request.user.addresses.all()
        return context


class CartItemUpdateView(
    CartItemMixin, CartItemUpdateDeleteSuccessUrl, UpdateView
):
    """View for updating a cart item.

    Inherits:
        - CartItemMixin: Handles cart item-specific logic.
        - CartItemUpdateDeleteSuccessUrl: Provides the URL after update.
        - UpdateView: Handles the update of a `CartItem`.

    Attributes:
        form_class (Form): The form for updating `CartItem`.
    """
    form_class = CartItemForm


class CartItemDeleteView(
    CartItemMixin, CartItemUpdateDeleteSuccessUrl, DeleteView
):
    """View for deleting a cart item.

    Inherits:
        - CartItemMixin: Handles cart item-specific logic.
        - CartItemUpdateDeleteSuccessUrl: Provides the URL after deletion.
        - DeleteView: Handles the deletion of a `CartItem`.
    """
    pass
