from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import MAX_LENTGH_ADDRESS_CONSTANTS
from catalog.models import Location


class CustomUser(AbstractUser):
    pass


class AddressUser(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='addresses'
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='addresses'
    )
    street = models.CharField(max_length=MAX_LENTGH_ADDRESS_CONSTANTS)
    postal_code = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return (
            f'{self.user.username} -'
            f'{self.location}, {self.street}, {self.postal_code}'
        )
