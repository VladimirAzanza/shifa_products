from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from .forms import ReviewForm
from .models import Product, Review


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.get_object().reviews.all()
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    pk_url_kwarg = 'product_id'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Product,
            pk=self.kwargs.get(self.pk_url_kwarg)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product = self.get_object()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.get_object().pk}
        )
