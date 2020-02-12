import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.forms import SearchCustomerForm, CustomerOrderForm

from rewards.clients.rewards_service_client import RewardsServiceClient

from .utils import is_email_valid

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.rewards_data =  rewards_service_client.get_rewards()

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rewards_data'] = self.rewards_data
        if request.method == "POST":

            form = CustomerOrderForm(request.POST)
            if form.is_valid():
                self.rewards_service_client.customer_order(form.cleaned_data['email_address'],form.cleaned_data['order_total'])
            else:
                context['add_order_error'] = 'form input invalid, vaild email and order total are expected. '

        context['customer_reward_info'] = self.rewards_service_client.get_all_customers_reward()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rewards_data'] = self.rewards_data
        # if input is empty return all the customer reward, if an email is entered, return single data match that record
        if request.method == "GET":
            form = SearchCustomerForm(request.GET)
            if form.is_valid():
                if form.cleaned_data['email_address']:
                    customer_reward_info = self.rewards_service_client.get_customer_reward(form.cleaned_data['email_address'])

                else:
                    customer_reward_info = self.rewards_service_client.get_all_customers_reward()

                if customer_reward_info:
                    context['customer_reward_info'] = customer_reward_info
            else:
                context['search_customer_error'] = 'please search with an email address.'

        return TemplateResponse(
            request,
            self.template_name,
            context
        )




