import logging, requests
from requests.structures import CaseInsensitiveDict

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
        context['rewards_data'] = self.rewards_service_client.get_rewards()
        context['add_points_endpoint'] = "http://localhost:7050/endpoint_one"
        context['user_data'] = self.rewards_service_client.get_all_user_data()
    
        
        

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
