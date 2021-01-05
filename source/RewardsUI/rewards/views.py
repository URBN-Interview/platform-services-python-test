import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

from django.http import HttpResponseRedirect


class RewardsView(TemplateView):
    template_name = "index.html"

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context["rewards_data"] = rewards_data

        email = request.GET.get("search")
        if email is None:
            customers_data = self.rewards_service_client.get_customers()
            
        else:
            customerSearchArr = []
            customerSearchArr.append(self.rewards_service_client.get_customer(email))
            customers_data = customerSearchArr
        context["customers_data"] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        email = request.POST.get("customerEmail")
        total = request.POST.get("orderTotal")
        orderData = {"email": email, "orderTotal": total}
        self.rewards_service_client.post_order(orderData)   

        return HttpResponseRedirect("/rewards")

