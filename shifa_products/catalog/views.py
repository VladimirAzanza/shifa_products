from django.views.generic import (
    DetailView,
    ListView,
)

from .models import Product


class ProductListView(ListView):
    template_name = 'catalog/product_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    pk_url_kwarg = 'product_id'
    template_name = 'catalog/product_detail.html'
