import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import EmailForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        # customers_data = self.rewards_service_client.get_customers()

        # context["customers_data"] = customers_data
        context['rewards_data'] = rewards_data

        if(request.method == 'GET'):
            form = EmailForm(request.GET)

            if(form.is_valid()):
                email = form.cleaned_data["email"]
                customers_data = self.rewards_service_client.get_customers(email)
                context["customers_data"] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
