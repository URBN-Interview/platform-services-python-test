from handlers.rewards_handler import RewardsHandler
from handlers.customer_order import CustomerOrder
from handlers.customer_request import CustomerRequest
from handlers.all_customers import AllCustomerRequests
url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerOrder), 
    (r'/customer', CustomerRequest),
    (r'/allcustomers', AllCustomerRequests)
]
