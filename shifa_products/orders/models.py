from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product
from shifa_products.constants import (
    DEFAULT_ORDER_STATUS, MAX_LENGHT_ORDER_STATUS, ORDER_STATUS_CHOICES
)
from users.models import AddressUser


User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Usuario'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    address = models.ForeignKey(
        AddressUser,
        related_name='orders',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Dirección de entrega'
    )
    status = models.CharField(
        max_length=MAX_LENGHT_ORDER_STATUS,
        choices=ORDER_STATUS_CHOICES,
        default=DEFAULT_ORDER_STATUS,
        verbose_name='Estado orden'
    )

    class Meta:
        verbose_name = 'Órden de compra'
        verbose_name_plural = 'Órdenes de compra'

    def __str__(self):
        return (
            f'Orden de {self.user.username} creada: {self.created_at.date()}'
        )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Órden de compra'
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Cantidad'
    )

    class Meta:
        verbose_name = 'Artículo en órden de compra'
        verbose_name_plural = 'Artículos en órden de compra'

    def __str__(self):
        return (
            f'Producto {self.product} en orden de {self.order.user.username}'
        )
