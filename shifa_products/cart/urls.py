from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path(
        '',
        views.CartDetailView.as_view(),
        name='cart'
    ),
    path(
        'add_to_cart/<int:product_id>/',
        views.AddToCartCreateView.as_view(),
        name='add_to_cart'
    ),
    path(
        'item/<int:cart_item_id>/',
        views.CartItemUpdateView.as_view(),
        name='update_cart_item'
    ),
    path(
        'item/<int:cart_item_id>/delete',
        views.CartItemDeleteView.as_view(),
        name='delete_cart_item'
    )
]
