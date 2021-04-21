import logging

import requests
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from .clients.rewards_service_client import RewardsServiceClient
from .forms import EmailForm, OrderForm
from django.shortcuts import redirect


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), **kwargs):
        super().__init__(**kwargs)
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self,request,*args,**kwargs):
        context = self.get_context_data(**kwargs)
        context["rewards_data"] = self.rewards_service_client.get_rewards()
        context["customers_data"] = self.rewards_service_client.get_Customers()

        if request.method == 'GET':
            form = EmailForm(request.GET)
            if form.is_valid():
                if form.cleaned_data["email"]:
                    email = form.cleaned_data["email"]
                    context["single_customers_data"] = self.rewards_service_client.get_Single_Customer(email)

                    if not context["single_customers_data"]:
                        context["customer_error"] = "Email does not exist"

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["orderEmail"]
                orders = form.cleaned_data["points"]
                requests.post("http://rewardsservice:7050/orders", data={"email": email, "orders": orders})
            else:
                print("NOT A VALID FORM")

            context["rewards_data"] = self.rewards_service_client.get_rewards()
            context["customers_data"] = self.rewards_service_client.get_Customers()

            return redirect("/rewards")

        return TemplateResponse(
            request,
            self.template_name,
            context
        )