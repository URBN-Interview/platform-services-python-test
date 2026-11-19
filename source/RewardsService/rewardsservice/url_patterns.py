from handlers.customers_handler import CustomerHandler, CustomersHandler
from handlers.orders_handler import OrdersHandler
from handlers.rewards_handler import RewardsHandler


def make_url_patterns(repository):
    kwargs = {"repository": repository}
    return [
        (r"/rewards/?", RewardsHandler, kwargs),
        (r"/orders/?", OrdersHandler, kwargs),
        (r"/customers/?", CustomersHandler, kwargs),
        (r"/customers/([^/]+)/?", CustomerHandler, kwargs),
    ]
