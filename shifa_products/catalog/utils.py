import logging

from PIL import Image

from shifa_products.constants import QUALITY_IMAGE

logger = logging.getLogger('admin_notifications')


def optimize_image(image):
    img = Image.open(image)
    logger.info(f"Imagen original tamaño: {image.size}")
    img.save(image.path, "JPEG", quality=QUALITY_IMAGE, optimize=True)
    logger.info(f"Imagen optimizada tamaño: {image.size}")
