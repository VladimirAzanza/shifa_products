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
    """View for listing all product categories.

    Inherits from:
        - ListView: Displays a list of 'Category' objects.

    Attributes:
        model (Model): The model associated with the view 'Category'.
        context_object_name (str): Name of the context variable.

    Methods:
        get_queryset():
            Returns all 'Category' objects.
    """
    model = Category
    context_object_name = 'categories'


class ProductListView(ListView):
    """View for listing products in a specific category.

    Inherits from:
        - ListView: Displays a list of 'Product' objects.

    Attributes:
        model (Model): The model associated with the view 'Product'.
        paginate_by (int): Number of products per page.
        context_object_name (str): Name of the context variable.

    Methods:
        get_category():
            Retrieves the category associated with the URL
            parameter 'category_slug'.

        get_queryset():
            Returns all products for the specific category.

        get_context_data(**kwargs):
            Adds additional context, such as the current category
            and a 'CartItemForm' instance.
    """
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
        context['form'] = CartItemForm()
        return context


class ProductSearchView(ListView):
    """View for searching products based on a query.

    Inherits from:
        - ListView: Displays a list of 'Product' objects.

    Attributes:
        model (Model): The model associated with the view 'Product`.
        context_object_name (str): Name of the context variable.

    Methods:
        get_query():
            Retrieves the search query from the GET request.

        get_queryset():
            Filters the products based on the search query.

        get_context_data(**kwargs):
            Adds additional context, such as the search query
            and an active search flag.
    """
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
    """View for displaying the details of a specific product.

    Inherits from:
        - DetailView: Displays a single `Product` object.

    Attributes:
        model (Model): The model associated with the view 'Product'.
        pk_url_kwarg (str): The URL keyword used to identify the product.

    Methods:
        get_queryset():
            Annotates products with average review ratings and review count.

        get_context_data(**kwargs):
            Adds product details, paginated reviews, and a 'CartItemForm'
            to the context.
    """
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
    """View for creating a review for a specific product.

    Inherits from:
        - LoginRequiredMixin: Ensures the user is authenticated.
        - CreateView: Handles the creation of a new 'Review' object.

    Attributes:
        model (Model): The model associated with the view 'Review'.
        form_class (Form): The form class used to create `Review`.
        pk_url_kwarg (str): The URL keyword used to identify the product.

    Methods:
        handle_no_permission():
            Handles the case when the user is not authenticated and shows
            a message.

        get_object():
            Retrieves the 'Product' object based on the 'product_id' from
            the URL.

        get():
            Verifies if the user has already submitted a review for the
            product, otherwise proceeds.

        get_context_data(**kwargs):
            Adds the 'Product' object to the context.

        form_valid(form):
            Sets the 'user' and 'product' fields on the 'Review' instance
            before saving.

        get_success_url():
            Returns the URL to redirect to after successfully creating
            the review.
    """
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
    """View for updating a review.

    Inherits from:
        - OnlyAuthorMixin: Restricts access to the review owner.
        - UpdateView: Handles updating an existing 'Review' object.

    Attributes:
        model (Model): The model associated with the view 'Review'.
        pk_url_kwarg (str): The URL keyword used to identify the review.
        form_class (Form): The form class used to update 'Review'..

    Methods:
        get_context_data(**kwargs):
            Adds the 'Product' object associated with the review to
            the context.

        get_success_url():
            Returns the URL to redirect to after successfully updating
            the review.
    """
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
    """View for deleting a review.

    Inherits from:
        - OnlyAuthorMixin: Restricts access to the review owner.
        - DeleteView: Handles the deletion of an existing 'Review' object.

    Attributes:
        model (Model): The model associated with the view 'Review'.
        pk_url_kwarg (str): The URL keyword argument used to identify the
        review.

    Methods:
        get_success_url():
            Returns the URL to redirect to after successfully deleting the
            review.
    """
    model = Review
    pk_url_kwarg = 'review_id'

    def get_success_url(self):
        return reverse_lazy(
            'catalog:product_detail',
            kwargs={'product_id': self.object.product.pk}
        )
