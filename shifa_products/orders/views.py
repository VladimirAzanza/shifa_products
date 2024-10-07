from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import OrderForm
from .models import Order
from cart.models import CartItem


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        cart_item = get_object_or_404(
            CartItem, cart__user=self.request.user
        )
        form.instance.cart_item = cart_item
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'pages:index'
        )
