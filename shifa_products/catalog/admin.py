from django.contrib import admin

from .constants import LENGTH_SHORT_REVIEW
from .models import Category, Location, Product, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'location',
    )
    list_display = (
        'id',
        'name',
        'description',
        'is_available',
        'price',
        'category',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'slug',
        'name'
    )
    search_fields = (
        'slug',
        'id'
    )
    list_editable = (
        'slug',
        'name'
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'short_review',
        'date',
        'taste_stars',
        'quality_stars',
        'product',
        'user',
        'location'
    )
    list_filter = (
        'location',
        'taste_stars',
        'quality_stars'
    )

    @admin.display(description='Reseña')
    def short_review(self, obj):
        return obj.review[:LENGTH_SHORT_REVIEW] + '...'


admin.site.empty_value_display = 'Campo sin rellenar'
