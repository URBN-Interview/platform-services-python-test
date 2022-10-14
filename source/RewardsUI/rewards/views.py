import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        email_address = request.GET.get('email_address')
        if email_address:
            customers_data = [self.rewards_service_client.get_customer(email_address)]
        else:
            customers_data = self.rewards_service_client.get_customers()

        context['customers_data'] = self.format_customers_data(customers_data)

        def customers_data_formatiing(self, customers_data):
            for customer in customers_data:
                if customer is None:
                    continue

                customer['next_reward_tier_progress'] = "{0:.0%}".format(customer['next_reward_tier_progress'])

                for key, value in customer.items():
                    if not value:
                        customer[key] = 'N/A'

            return customers_data