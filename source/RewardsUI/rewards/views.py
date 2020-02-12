import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.forms import SearchCustomerForm, CustomerOrderForm

from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print('herererererer')
        if request.method == "POST":
            form = CustomerOrderForm(request.POST)
            if form.is_valid():
                self.rewards_service_client.customer_order(form.cleaned_data['email_address'],form.cleaned_data['order_total'])

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        if request.method == "GET":
            form = SearchCustomerForm(request.GET)
            if form.is_valid():
                if form.cleaned_data['email_address']:
                    customer_reward_info = self.rewards_service_client.get_customer_reward(form.cleaned_data['email_address'])
                    print('here 29')
                else:
                    customer_reward_info = self.rewards_service_client.get_all_customers_reward()
                    print('here 339389383')
                if customer_reward_info:
                    context['customer_reward_info'] = customer_reward_info
                print('what')
                print(customer_reward_info)
            else:
                print('debug1')
                print(form)
                print(dir(form))
        else:
            print('debug 2')

        return TemplateResponse(
            request,
            self.template_name,
            context
        )




