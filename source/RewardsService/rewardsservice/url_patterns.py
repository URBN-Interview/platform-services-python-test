from handlers.rewards_handler import RewardsHandler
from handlers.customers_handler import customersHandler
from handlers.orders_handler import ordersHandler
from handlers.specific_customer_handler import specific_customerHandler
url_patterns = [

    (r'/rewards', RewardsHandler),
    (r'/customers', customersHandler),
    (r'/orders', ordersHandler),
    (r'/customer',specific_customerHandler)
]

"""
    ex. www.localhost:7050/rewards
    ex2. www.localhost:7050/customers
    ex3. www.localhost:7050/orders?email=sarthak@gmail.com&orders=301
    ex4. www.localhost:7050/customer?email=sarthak@gmail.com
    
"""