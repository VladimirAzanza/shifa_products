from django.contrib.auth import get_user_model
from django.db import models

from cart.models import CartItem
from users.models import AddressUser


class Order(models.Model):
    cart_item = models.OneToOneField(
        CartItem,
        on_delete=models.CASCADE,
        related_name='order'
    )
    address = models.ForeignKey(
        AddressUser,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
