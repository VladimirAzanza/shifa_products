from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path(
        'checkout/',
        views.OrderCreateView.as_view(),
        name='checkout'
    ),
]