from handlers.rewards_handler import RewardsHandler, ManageCustomer, GetCustomer, GetAllCustomers

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/manage_customer', ManageCustomer),
    (r'/get_customer/([^/]+)', GetCustomer),
    (r'/get_all_customers', GetAllCustomers),
]
