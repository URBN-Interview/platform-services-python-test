from rewardsservice.handlers.base_handler import ApiError, BaseHandler
from rewardsservice.helpers.validation import ValidationError, parse_order_body
from rewardsservice.helpers import rewards_calculator
from rewardsservice.repositories.customers_repository import CustomersRepository
from rewardsservice.repositories.rewards_repository import RewardsRepository

class CustomerDataHandler(BaseHandler):

    def initialize(self, customer_repo: CustomersRepository, rewards_repo: RewardsRepository):
        self.customer_repo = customer_repo
        self.rewards_repo = rewards_repo

    async def get(self, email):
        customer = await self.customer_repo.get_customer(email)
        if not customer:
            raise ApiError(404, "customer not found")
        self.write_json(customer)

    async def post(self):
        try:
            email, order_total = parse_order_body(self.request.body)
        except ValidationError as exc:
            raise ApiError(400, str(exc))

        tiers = await self.rewards_repo.get_all_tiers()
        points_earned = rewards_calculator.get_rewards_points_for_purchase(order_total)

        customer = await self.customer_repo.get_customer(email)
        if not customer:
            customer_points = points_earned
        else:
            customer_points = customer["reward_points"] + points_earned

        rewards_fields = rewards_calculator.customer_rewards_fields(customer_points, tiers)

        updated_customer = await self.customer_repo.update_customer(email, {
                                                                        "reward_points": customer_points,
                                                                        **rewards_fields,
                                                                    })
        self.write_json(updated_customer, status=201)
        
class CustomersDataHandler(BaseHandler):
    def initialize(self, customer_repo: CustomersRepository):
        self.customer_repo = customer_repo
        
    async def get(self):
        customers = await self.customer_repo.get_all_customers()
        self.write_json(customers)

