import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.customer_rewards_client import CustomerRewardsClient

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), customer_rewards_client=CustomerRewardsClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.customer_rewards_client = customer_rewards_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        customer_data = self.customer_rewards_client.get_customer_list()
        context['rewards_data'] = rewards_data
        context['customer_data'] = customer_data
        query_dict = request.GET
        email = query_dict.get("email")
        if email is not None:
            customer_rewards = self.customer_rewards_client.get_customer(email)
            context['customer_rewards'] = customer_rewards

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, **kwargs):
        if request.method == "POST":
            email = request.POST.get("email")
            order = request.POST.get("order")
            response = self.customer_rewards_client.update_customer_rewards(email, order)
            if response:
                context = {}
                rewards_data = self.rewards_service_client.get_rewards()
                customer_data = self.customer_rewards_client.get_customer_list()
                context['rewards_data'] = rewards_data
                context['customer_data'] = customer_data
            else:
                return HttpResponse("PUT was unsuccessful")

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
