from handlers.rewards_handler import RewardsHandler, ManageCustomer, GetCustomer

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/manage_customer', ManageCustomer),
    (r'/get_customer/([^/]+)', GetCustomer),
]
