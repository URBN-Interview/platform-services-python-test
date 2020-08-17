from handlers.rewards_handler import RewardsHandler
from handlers.landing_page import LandingPage

url_patterns = [
	(r'/', LandingPage),
    (r'/rewards', RewardsHandler),
]
