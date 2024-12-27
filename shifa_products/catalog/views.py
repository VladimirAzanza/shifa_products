from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .forms import ReviewForm
from .mixins import OnlyAuthorMixin
from .models import Category, Product, Review
from cart.forms import CartItemForm
from shifa_products.constants import (
    MAX_REVIEWS_MESSAGE, SIGN_IN_TO_ADD_REVIEW_MESSAGE
)


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'

    def get_category(self):
        return get_object_or_404(
            Category, slug=self.kwargs.get('category_slug')
        )

    def get_queryset(self):
        return Product.objects.filter(
            category=self.get_category()
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class ProductSearchView(ListView):
    model = Product
    context_object_name = 'products'

    def get_query(self):
        return self.request.GET.get('q')

    def get_queryset(self):
        query = self.get_query()
        object_list = Product.objects.filter((
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(category__slug__icontains=query)
            ) & Q(is_available=True)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_active'] = True
        context['query'] = self.get_query()
        return context


class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'product_id'

    def get_queryset(self):
        return Product.objects.annotate(
            avg_quality_stars=Avg('reviews__quality_stars'),
            avg_taste_stars=Avg('reviews__taste_stars'),
            review_count=Count('reviews')
        ).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_object().reviews.all(), 3)
        page = self.request.GET.get('page')
        context['reviews'] = paginator.get_page(page)
        context['form'] = CartItemForm()
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    pk_url_kwarg = 'product_id'

    def handle_no_permission(self):
        messages.error(self.request, SIGN_IN_TO_ADD_REVIEW_MESSAGE)
        return super().handle_no_permission()

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
