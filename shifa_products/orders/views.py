from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import OrderForm
from .mixins import OnlyAuthorOrderMixin
from .models import Order, OrderItem
from cart.models import Cart


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        order = form.save()
        cart = get_object_or_404(
            Cart, user=self.request.user
        )
        cart_items = cart.cart_items.all()
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        cart.delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'orders:order_detail',
            kwargs={'order_id': self.object.pk}
        )


class OrderDetailView(OnlyAuthorOrderMixin, DetailView):
    model = Order
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.get_object().order_items.annotate(
            total_item=F('quantity') * F('product__price')
        )
        context['order_total'] = self.get_object().order_items.aggregate(
            order_total=Sum(F('quantity') * F('product__price'), default=0)
        )['order_total']
        return context


class OrderListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
