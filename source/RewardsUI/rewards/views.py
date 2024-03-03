import logging

from django.utils.http import urlencode
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
        email = request.GET.get("email", "")
        customers_data = self.rewards_service_client.get_customer_rewards(email=email)
        context.update({
            "rewards_data": rewards_data,
            "customers_data": customers_data,
            "user_email": email,
        })

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        email = request.POST.get("user_email")
        if email:
            parameters = urlencode({"email": email})
            return redirect("{}?{}".format(reverse("rewards"), parameters))
        form = AddRewardsForm(request.POST)
        if form.is_valid():
            data = {
                "emailId": form.cleaned_data["email"],
                "orderTotal": form.cleaned_data["total"],
            }
            data = self.rewards_service_client.add_order(data)
            return redirect(reverse("rewards"))
        return redirect(reverse("rewards"))
