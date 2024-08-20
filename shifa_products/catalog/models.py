from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
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
    name = models.CharField(max_length=100)
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
