from django.db import models

from .constants import MAX_LENGTH_NAME


class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        help_text=(
            'Required identifier for category URL;'
            'Symbols, dashes, or underscores are acceptable.'
        )
    )


class Location(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)


class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    description = models.TextField()
    image = models.ImageField(upload_to='products/images/')
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True
    )
    location = models.ManyToManyField(
        Location,
        related_name='products'
    )
    # reviews
