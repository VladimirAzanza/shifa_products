from django.forms import ValidationError
from PIL import Image

from shifa_products.constants import (
    HEIGHT_SIZE_IMAGE,
    IMAGE_FORMAT_MESSAGE,
    IMAGE_SIZE_MESSAGE,
    RATING_MESSAGE,
    WIDTH_SIZE_IMAGE
)


def validate_stars(stars):
    if stars < 1 or stars > 5:
        raise ValidationError(RATING_MESSAGE)
    return stars


def validate_image(image):
    valid_formats = ['JPEG']
    img = Image.open(image)
    if img.format not in valid_formats:
        raise ValidationError(IMAGE_FORMAT_MESSAGE)
    if img.size[0] > WIDTH_SIZE_IMAGE or img.size[1] > HEIGHT_SIZE_IMAGE:
        raise ValidationError(IMAGE_SIZE_MESSAGE)
