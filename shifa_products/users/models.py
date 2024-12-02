from django.contrib.auth.models import AbstractUser
from django.db import models

from shifa_products.constants import MAX_LENTGH_ADDRESS_CONSTANTS


class CustomUser(AbstractUser):
    email = models.EmailField('correo electrónico', unique=True)
    first_name = models.CharField('nombre', max_length=150)
    last_name = models.CharField('apellido', max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name', 'password'
    ]


class AddressUser(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='addresses'
    )
    location = models.ForeignKey(
        'catalog.Location', on_delete=models.CASCADE, related_name='addresses'
    )
    street = models.CharField(max_length=MAX_LENTGH_ADDRESS_CONSTANTS)
    postal_code = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return (
            f'{self.location}, {self.street}, {self.postal_code}'
        )
