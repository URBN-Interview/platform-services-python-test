import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.endpoint1_client import Endpoint1Client

# grab all rewards
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

# add order
class AddOrderView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), endpoint1_client=Endpoint1Client()):
        self.logger = logger
        self.endpoint1_client = endpoint1_client

    def post(self, email, order_total, request, **kwargs):
        # self.email = email
        # self.order_total = order_total
        if request.method == 'POST':
            email = request.POST.get("email")
            order_total = request.POST.get("order_total")
        
        context = self.get_context_data(**kwargs)

        order_data = self.endpoint1_client.add_order(email, order_total)
        context['email'] = order_data
        context['order_total'] = order_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )


# search for user
class SearchForUserView(TemplateView):
    template_name = 'index.html'
