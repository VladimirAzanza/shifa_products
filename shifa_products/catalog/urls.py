from django.urls import include, path

from . import views

app_name = 'catalog'

product_urls = [
    path(
        '<int:product_id>/',
        views.ProductDetailView.as_view(),
        name='product_detail'
    ),
    path(
        '<int:product_id>/review/',
        views.ReviewCreateView.as_view(),
        name='review_form'
    ),
    path(
        '<int:product_id>/review/<int:review_id>',
        views.ReviewUpdateView.as_view(),
        name='review_update'
    ),
    path(
        '<int:product_id>/delete_review/<int:review_id>',
        views.ReviewDeleteView.as_view(),
        name='review_delete'
    )
]

category_urls = [
    path(
        '',
        views.CategoryListView.as_view(),
        name='category_list'
    ),
    path(
        '<slug:category_slug>/',
        views.ProductListView.as_view(),
        name='category_product_list'
    )
]

urlpatterns = [
    path(
        'category/', include(category_urls)
    ),
    path(
        'product/', include(product_urls)
    ),
    path(
        'search/',
        views.ProductSearchView.as_view(),
        name='product_search'
    ),
]
