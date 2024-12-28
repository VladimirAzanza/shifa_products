from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path(
        '',
        views.OrderListView.as_view(),
        name='orders_list'
    ),
    path(
        'detail/<int:order_id>/',
        views.OrderDetailView.as_view(),
        name='order_detail'
    ),
    path(
        'detail/<int:order_id>/pdf',
        views.OrderPdfPrintView.as_view(),
        name='order_pdf'
    ),
    path(
        'checkout/',
        views.OrderCreateView.as_view(),
        name='checkout'
    ),
]
