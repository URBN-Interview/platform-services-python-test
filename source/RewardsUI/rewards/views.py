import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django import forms

from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        customers_data = self.rewards_service_client.get_customers()

        if request.method == 'GET':
            form = SearchForm(request.GET)
            # replace list of all customers with the curstomer found from email search, might return nothing for customers
            if form.is_valid():
                customer_data = self.rewards_service_client.get_customer(form.cleaned_data['email_address'])
                context['rewards_data'] = rewards_data
                context['customers_data'] = customer_data
            # form info was invalid or empty, use original tables
            else:
                context['rewards_data'] = rewards_data
                context['customers_data'] = customers_data
        else:
            # original table info to load
            context['rewards_data'] = rewards_data
            context['customers_data'] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.method == 'POST':
            form = OrderForm(request.POST)
            # add or update customer order info
            if form.is_valid():
                self.rewards_service_client.add_order_rewards(form.cleaned_data['order_email_address'], form.cleaned_data['order_total'])
        # original table info to load
        rewards_data = self.rewards_service_client.get_rewards()
        customers_data = self.rewards_service_client.get_customers()
        context['rewards_data'] = rewards_data
        context['customers_data'] = customers_data
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

class SearchForm(forms.Form):
    email_address = forms.CharField(label="Email Address", max_length=254)

class OrderForm(forms.Form):
    order_email_address = forms.CharField(label="Email Address", max_length=254)
    order_total = forms.FloatField(label="Order Total")