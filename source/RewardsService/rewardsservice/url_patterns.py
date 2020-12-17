from handlers.order_handler import OrderHandler
from handlers.customer_handler import CustomerHandler
from handlers.customers_handler import CustomersHandler

url_patterns = [
    (r'/order', OrderHandler),
    (r'/customer', CustomerHandler),
    (r'/customers', CustomersHandler),
]
