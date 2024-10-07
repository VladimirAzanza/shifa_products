from django.contrib.auth import get_user_model
from django.db import models

from cart.models import CartItem
from catalog.models import Product


class Order(models.Model):
    cart_item = models.OneToOneField(
        CartItem,
        on_delete=models.CASCADE,
        related_name='order'
    )
    created_at = models.DateTimeField(auto_now_add=True)
