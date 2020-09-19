import logging

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

from .forms import OrderForm, FilterForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        customers_data = self.rewards_service_client.get_customers()
        context['customers_data'] = customers_data

        filterForm = FilterForm(request.GET)
        context['filterForm'] = filterForm

        if filterForm.is_valid():
            email = filterForm.cleaned_data.get("email")
            customers_data = self.rewards_service_client.get_customer(email)
            context['customers_data'] = [customers_data]

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        orderForm = OrderForm(request.POST)
        context['orderForm'] = orderForm

        if orderForm.is_valid():
            email = orderForm.cleaned_data.get("email")
            total = orderForm.cleaned_data.get("total")
            self.rewards_service_client.add_customers(email, total)
            return HttpResponseRedirect("/rewards")
