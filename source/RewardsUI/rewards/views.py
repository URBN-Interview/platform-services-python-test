import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.forms import SearchCustomerForm, CustomerOrderForm

from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()

        context['rewards_data'] = rewards_data

        if request.method == "GET":
            form = SearchCustomerForm(request.GET)
            if form.is_valid():

                customer_reward_info = self.rewards_service_client.get_customer_reward(form.cleaned_data['email_address'])
                if customer_reward_info and 'error' not in customer_reward_info:
                    context['customer_reward_info'] = customer_reward_info

                print(customer_reward_info)
            else:
                print('debug1')
        else:
            print('debug 2')

        return TemplateResponse(
            request,
            self.template_name,
            context
        )




