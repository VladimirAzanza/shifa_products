from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import OrderForm
from .models import Order
from cart.models import Cart, CartItem


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        cart = get_object_or_404(
            Cart, user=self.request.user
        )
        form.instance.cart = cart
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'orders:order_detail',
            kwargs={'order_id': self.object.pk}
        )


class OrderDetailView(DetailView):
    model = Order
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.object.cart
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        return context
