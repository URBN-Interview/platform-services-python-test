from handlers.order_handler import OrderHandler
from handlers.customer_handler import CustomerHandler

url_patterns = [
    (r'/order', OrderHandler),
    (r'/customer', CustomerHandler),
]
