from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AddToCartForm
from .models import CartItem
from catalog.models import Product


class AddToCartCreateView(LoginRequiredMixin, CreateView):
    model = CartItem
    form_class = AddToCartForm
    pk_url_kwarg = 'product_id'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Product,
            pk=self.kwargs.get(self.pk_url_kwarg)
        )

    def form_valid(self, form):
        form.instance.product = self.get_object()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.object.product.pk}
        )
