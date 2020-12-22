import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render

from rewards.clients.rewards_service_client import RewardsServiceClient, CustomerRewardsClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.POST.get("email") is not None:
            email = request.POST.get('email_address')
            amount = request.POST.get('amount')

        post_rewards = self.rewards_service_client.post_rewards(email, amount)
        context['rewards_data'] = post_rewards
        return render(request, self.template_name, context)

#
# class RewardsView(TemplateView):
#     template_name = 'index.html'
#
#     def __init__(self, logger=logging.getLogger(__name__),customer_rewards_client=CustomerRewardsClient()):
#         self.logger = logger
#         self.customer_rewards_client = customer_rewards_client
#
#     def get(self, request, **kwargs):
#         context = self.get_context_data(**kwargs)
#
#         customer_email = request.POST.get("customer_email")
#         customer_data = self.customer_rewards_client.get_customers(customer_email)
#         context['customer_data'] = customer_data
#
#         return TemplateResponse(request, self.template_name, context)
