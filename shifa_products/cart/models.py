from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product


User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrito de {self.user.username} creado: {self.created_at}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        default=1, verbose_name='Cantidad'
    )

    def __str__(self):
        return f'Producto {self.product} en carrito de {self.cart.user.username}'
