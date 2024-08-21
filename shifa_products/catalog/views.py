from django.views.generic import (
    DetailView,
    ListView,
)

from .models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'product_id'
