from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_LENGTH_NAME, MAX_LENGTH_REVIEW, MAX_LENGTH_TITLE


User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_NAME)

    class Meta:
        abstract = True


class Category(BaseModel):
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        help_text=(
            'Required identifier for category URL;'
            'Symbols, dashes, or underscores are acceptable.'
        )
    )

    def __str__(self):
        return self.name


class Location(BaseModel):
    pass

    def __str__(self):
        return self.name


class Product(BaseModel):
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

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_TITLE)
    review = models.CharField(max_length=MAX_LENGTH_REVIEW)
    date = models.DateTimeField(auto_now_add=True)
    taste_stars = models.IntegerField(default=5)
    quality_stars = models.IntegerField(default=5)
    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_name_owner'
            )
        ]
        ordering = ['-date']

    def __str__(self):
        return self.title
