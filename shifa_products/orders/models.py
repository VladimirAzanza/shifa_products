from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product
from users.models import AddressUser


User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(
        AddressUser,
        related_name='orders',
        on_delete=models.PROTECT,
        null=True
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(verbose_name='Cantidad')
