import logging

from django.urls import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.forms import AddRewardsForm
from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        customers_data = self.rewards_service_client.get_customer_rewards()
        context['rewards_data'] = rewards_data
        context['customers_data'] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        form = AddRewardsForm(request.POST)
        if form.is_valid():
            data = {
                "emailId": form.cleaned_data["email"],
                "orderTotal": form.cleaned_data["total"],
            }
            data = self.rewards_service_client.add_order(data)
            return redirect(reverse("rewards"))
        return redirect(reverse("rewards"))
