from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path(
        'detail/<int:order_id>/',
        views.OrderDetailView.as_view(),
        name='order_detail'
    ),
    path(
        'checkout/',
        views.OrderCreateView.as_view(),
        name='checkout'
    ),
]
