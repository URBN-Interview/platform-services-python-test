from handlers.rewards_handler import RewardsHandler
from handlers.landing_page import LandingPage
from handlers.customer_handler import CustomerHandler
from handlers.all_customers import AllCustomers

url_patterns = [
	(r'/', LandingPage),
    (r'/rewards', RewardsHandler),
    (r'/customer', CustomerHandler),
    (r'/allcustomers', AllCustomers)
]