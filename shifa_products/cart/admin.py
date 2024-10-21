from django.contrib import admin

from . models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at'
    )
    search_fields = (
        'user__username',
        'id'
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'product'
    )
    search_fields = (
        'cart__user__username',
        'product__name'
    )


admin.site.empty_value_display = 'Campo sin rellenar'
