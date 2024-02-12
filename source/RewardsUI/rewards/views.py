import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

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

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
   
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        order_total = request.POST.get('order_total')

        data = {
            'email': email,
            'order_total': order_total
        }

        # Making the POST request to the endpoint
        response = self.rewards_service_client.add_orders(data)

        if response.status_code == 201:
            print("Customer order data stored successfully.")
            rewards_data = response.json() 
            context = self.get_context_data(**kwargs)
            context['rewards_data'] = rewards_data
            return TemplateResponse(
                request,
                self.template_name,
                context
            )
        else:
            context = self.get_context_data(**kwargs)
            context['error_message'] = "Failed to store customer order data."
            return TemplateResponse(
                request,
                self.template_name,
                context
            )
