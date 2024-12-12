from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_image
from shifa_products.constants import (
    HELP_TEXT_SLUG, MAX_LENGTH_NAME, MAX_LENGTH_REVIEW, MAX_LENGTH_TITLE
)


User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Nombre'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    slug = models.SlugField(
        unique=True,
        help_text=(HELP_TEXT_SLUG)
    )

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(BaseModel):
    pass

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        ordering = ['id']

    def __str__(self):
        return self.name


class Product(BaseModel):
    description = models.TextField(
        verbose_name='Descripción'
    )
    image = models.ImageField(
        upload_to='products/images/',
        verbose_name='imagen',
        validators=(validate_image,)
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Disponible'
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Precio'
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Categoría'
    )
    location = models.ManyToManyField(
        Location,
        related_name='products',
        verbose_name='Localidad'
    )

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(
        max_length=MAX_LENGTH_TITLE,
        verbose_name='Título'
    )
    review = models.CharField(
        max_length=MAX_LENGTH_REVIEW,
        verbose_name='Reseña'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    taste_stars = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Sabor'
    )
    quality_stars = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Calidad'
    )
    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Producto'
    )
    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='usuario'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='localidad'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_name_owner'
            )
        ]
        ordering = ['-date']
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'

    def __str__(self):
        return self.title
