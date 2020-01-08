from handlers.rewards_handler import RewardsHandler
from handlers.customer_rewards_info_handler import CustomerInfoHandler
from handlers.all_customers_handler import AllCustomersHandler
from handlers.single_customer_handler import SingleCustomerHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/addorder', CustomerInfoHandler),
    (r'/allcustomerpoints', AllCustomersHandler),
    (r'/rewardssearch', SingleCustomerHandler),
]
