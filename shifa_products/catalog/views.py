from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .constants import MAX_REVIEWS_MESSAGE
from .forms import ReviewForm
from .mixins import OnlyAuthorMixin
from .models import Product, Review


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'product_id'

    def get_queryset(self):
        return Product.objects.annotate(
            avg_quality_stars=Avg('reviews__quality_stars'),
            avg_taste_stars=Avg('reviews__taste_stars'),
            review_count=Count('reviews')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_object().reviews.all(), 3)
        page = self.request.GET.get('page')
        context['reviews'] = paginator.get_page(page)
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

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if Review.objects.filter(user=request.user, product=product):
            messages.error(
                request,
                MAX_REVIEWS_MESSAGE
            )
            return redirect('catalog:product_detail', product_id=product.pk)
        return super().get(request, *args, **kwargs)

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


class ReviewUpdateView(OnlyAuthorMixin, UpdateView):
    model = Review
    pk_url_kwarg = 'review_id'
    template_name = 'catalog/review_form.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.object.product.pk}
        )


class ReviewDeleteView(OnlyAuthorMixin, DeleteView):
    model = Review
    pk_url_kwarg = 'review_id'

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.object.product.pk}
        )
