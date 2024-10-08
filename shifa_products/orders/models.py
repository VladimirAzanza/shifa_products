from django.contrib.auth import get_user_model
from django.db import models

from cart.models import Cart
from users.models import AddressUser


class Order(models.Model):
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
        related_name='order',
        null=True
    )
    address = models.ForeignKey(
        AddressUser,
        on_delete=models.CASCADE,
        related_name='order',
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
