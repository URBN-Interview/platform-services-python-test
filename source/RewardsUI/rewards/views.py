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
        context['customers'] = self.rewards_service_client.get_customers()
        return TemplateResponse(
            request,
            self.template_name,
            context
        )


class CustomerRewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data 
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email = request.POST.get("email")
        context['customers'] = self.rewards_service_client.get_customers()
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email = request.POST.get("email")
        order_total = request.POST.get("order_total")
        self.rewards_service_client.process_order(email, order_total)
        context['customers'] = self.rewards_service_client.get_customers()
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

class CustomerSearchView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data 
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email = request.POST.get("email")
        if email:
            context['customers'] = self.rewards_service_client.get_customer_data(email)
            print("@@@@@@@@@@@@@@", context['customers'])
        else:
            context['customers'] = self.rewards_service_client.get_customers()
        return TemplateResponse(
            request,
            self.template_name,
            context
        )