import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponseServerError

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.forms import OrderForm, UserFilterForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            rewards_data = self.rewards_service_client.get_rewards()
            customers_data = self.rewards_service_client.get_customers()
        except HttpResponseServerError as e:
            rewards_data = []
            customers_data = []

        context['rewards_data'] = rewards_data
        context['customers_data'] = customers_data
        context['order_form'] = OrderForm()
        context['filter_form'] = UserFilterForm()

        filter_form = UserFilterForm(request.GET)
        if filter_form.is_valid():
            filter_email = filter_form.cleaned_data["email"]
            try:
                customer_filter = self.rewards_service_client.get_filtered_customer(filter_email)
                if len(customer_filter) > 0:
                    context['customers_data'] = customer_filter
            except HttpResponseServerError as e:
                self.logger.error('No customer found with email: ' + filter_email + ', aborting...')

        for customer in context['customers_data']:
            customer['nextTierProgress'] = int(customer['nextTierProgress'] * 100)

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request):
        if request.method == "POST":
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order_email = order_form.cleaned_data["email"]
                order_total = order_form.cleaned_data["order_total"]
                self.rewards_service_client.add_order(order_email, order_total)

                return HttpResponseRedirect('/rewards')
