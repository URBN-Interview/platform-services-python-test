from handlers.rewards_handler import RewardsHandler
from handlers.landing_page import LandingPage
from handlers.customer_handler import CustomerHandler

url_patterns = [
	(r'/', LandingPage),
    (r'/rewards', RewardsHandler),
    (r'/customers', CustomerHandler)
]
