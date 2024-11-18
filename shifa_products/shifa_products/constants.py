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
