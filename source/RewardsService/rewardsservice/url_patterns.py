from handlers.rewards_handler import RewardsHandler
from handlers.order_handler import OrderHandler
from handlers.users_handler import UsersHandler

url_patterns = [
    (r'/rewards', RewardsHandler),
    #created order route
    (r'/order', OrderHandler), 
    #created users route
    (r'/users', UsersHandler), 
]
