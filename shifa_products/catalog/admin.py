from django.contrib import admin

from .models import Category, Location, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'is_available',
        'price',
        'category_id',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'slug',
    )
    search_fields = (
        'slug',
        'id'
    )
    list_editable = (
        'slug',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    search_fields = (
        'name',
        'id'
    )
    list_editable = (
        'name',
    )


admin.site.empty_value_display = 'Campo sin rellenar'
