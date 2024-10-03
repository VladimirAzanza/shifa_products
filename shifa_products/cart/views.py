from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import CartItemForm
from .mixins import OnlyAuthorCartItemMixin
from .models import Cart, CartItem
from catalog.mixins import OnlyAuthorMixin
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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.object.product.pk}
        )


class CartDetailView(OnlyAuthorMixin, DetailView):
    def get_object(self, queryset=None):
        return get_object_or_404(
            Cart,
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_item'] = self.get_object().cart_item.annotate(
            total_item=F('quantity') * F('product__price')
        )
        return context


class CartUpdateView(OnlyAuthorCartItemMixin, UpdateView):
    model = CartItem
    pk_url_kwarg = 'cart_item_id'
    form_class = CartItemForm

    def get_success_url(self):
        return reverse_lazy('cart:cart')
