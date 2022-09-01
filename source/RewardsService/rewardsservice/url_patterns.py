from handlers.rewards_handler import RewardsHandler
from handlers.customer_order_data_handler import CustomerOrderDataHandler
from handlers.customer_rewards_handler import CustomerRewardsHandler, SingleCustomerRewardsDataHandler


url_patterns = [
    (r'/rewards', RewardsHandler),

    # endpoint to create new customer order 
    (r'/customerOrderData', CustomerOrderDataHandler),

    # endpoint to retrieve all customer rewards data
    (r'/customerRewardsData', CustomerRewardsHandler),

    #endpoint to retrieve customer rewards data for user given email address
    (r'/singleCustomerRewardsData', SingleCustomerRewardsDataHandler)
]
