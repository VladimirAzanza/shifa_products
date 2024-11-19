from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path(
        '',
        views.CategoryListView.as_view(),
        name='category_list'
    ),
    path(
        '<slug:category_slug>/',
        views.ProductListView.as_view(),
        name='product_list'
    ),
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
