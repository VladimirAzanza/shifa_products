from django.views.generic import (
    DetailView,
    ListView,
)

from .models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 10


class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = 'product_id'
    template_name = 'catalog/product_detail.html'
