from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product


User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='Usuario'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    class Meta:
        verbose_name = 'Carrito de compra'
        verbose_name_plural = 'Carritos de compra'

    def __str__(self):
        return f'Carrito de {self.user.username} creado: {self.created_at.date()}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='cart_items',
        on_delete=models.CASCADE,
        verbose_name='Carrito de compra'
    )
    product = models.ForeignKey(
        Product,
        related_name='cart_items',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )
    quantity = models.PositiveSmallIntegerField(
        default=1, verbose_name='Cantidad'
    )

    class Meta:
        verbose_name = 'Artículo en carrito'
        verbose_name_plural = 'Artículos en carrito'

    def __str__(self):
        return (
            f'Producto {self.product} en carrito de {self.cart.user.username}'
        )
