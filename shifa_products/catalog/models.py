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


class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)
    description = models.TextField()
    image = models.ImageField(upload_to='products/images/')
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True
        )
    # is_available
    # location
    # reviews
