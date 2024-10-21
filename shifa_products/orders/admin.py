from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_at',
        'address'
    )
    search_fields = (
        'user__username',
        'id'
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity'
    )
    search_fields = (
        'order__user__username',
        'product__name'
    )


admin.site.empty_value_display = 'Campo sin rellenar'
