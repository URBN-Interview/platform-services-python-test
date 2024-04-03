from handlers.rewards_handler import *

url_patterns = [
    (r"/rewards", RewardsHandler), # default rewards handler 
    (r"/customer_data/add", AddCustomerDatahandler),  # End point to add/update the customer data wrt customer email and order
    (r"/customer_data/fetch/([^/]+)", FetchCustomerDatahandler),  # End point to fetch one customer data from DB
    (r"/customer_data/fetch/all", FetchAllCustomerDatahandler), # End point to fetch all the customer data from DB
]
