from handlers.rewards_handler import RewardsHandler, ManageCustomer

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/manage_customer', ManageCustomer),
]
