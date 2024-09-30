from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path(
        'add_to_cart/<int:product_id>/',
        views.AddToCartCreateView.as_view(),
        name='add_to_cart'
    )
]
