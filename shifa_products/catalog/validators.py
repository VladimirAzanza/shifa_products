from django.forms import ValidationError

from shifa_products.constants import RATING_MESSAGE


def validate_stars(stars):
    if stars < 1 or stars > 5:
        raise ValidationError(RATING_MESSAGE)
    return stars
