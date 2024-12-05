import os

# Constants for orders
MAX_LENGHT_ORDER_STATUS = 20
ORDER_STATUS_CHOICES = [
    ('PENDING', 'Pendiente'),
    ('PROCESSING', 'Procesando'),
    ('SHIPPED', 'Enviado'),
    ('DELIVERED', 'Entregado'),
    ('CANCELLED', 'Cancelado'),
]
DEFAULT_ORDER_STATUS = 'PROCESSING'
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_MESSAGE = 'Nuevo pedido de: {first_name} {last_name}'

# Constants for cart
SUCCESFUL_ADD_T0_CART_MESSAGE = 'El producto ha sido agregado a tu carrito.'
SIGN_IN_TO_ADD_CART_MESSAGE = 'Inicia sesión para añadir productos al carrito.'

# Constants for catalog
MAX_LENGTH_NAME = 100
MAX_LENGTH_TITLE = 100
MAX_LENGTH_REVIEW = 300
MAX_REVIEWS_MESSAGE = (
    'Solo se permite una reseña por cliente para este producto.'
)
RATING_MESSAGE = 'La calificación no puede ser menor a 1 ni mayor a 5'
SIGN_IN_TO_ADD_REVIEW_MESSAGE = (
    'Inicia sesión para añadir una reseña al producto.'
)
HELP_TEXT_SLUG = (
    'Identificador requerido para la URL de la categoría;'
    ' Se aceptan símbolos, guiones o guiones bajos.'
)
LENGTH_SHORT_REVIEW = 20

# Constants for users
MAX_LENTGH_ADDRESS_CONSTANTS = 100
ADDRESS_AT_ORDERS_MESSAGE = (
    'No se puede eliminar la dirección seleccionada'
    ' porque está asociada a una órden.'
)

# Constants for telegram tawk.to chat
TELEGRAM_TAWKTO_MESSAGE = (
    '🚀 Chat {status} en Tawk.to\n'
    '👤 Usuario: {visitor_name}\n'
    '🌍 País: {visitor_country}\n'
)
