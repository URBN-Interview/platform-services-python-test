import logging

from django.shortcuts import render
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.forms import RewardForm, CustomerForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, **kwargs):
        form = RewardForm()
        customer_form = CustomerForm()

        context = self.get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        context['form'] = form
        context['customer_form'] = customer_form
        context['table_1_visibility'] = "invisible"
        context['table_2_visibility'] = "invisible"

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = RewardForm()
        customer_form = CustomerForm()

        email_address = ""
        amount = 0

        if request.method == 'POST':
            form = RewardForm(request.POST)
            if form.is_valid():
                email_address = form.cleaned_data['email_address']
                amount = form.cleaned_data["amount"]

                post_rewards = self.rewards_service_client.post_rewards(email_address, amount)
                context['table_1_visibility'] = "visible"
                context['table_2_visibility'] = "invisible"
                context['data'] = post_rewards
                context['message'] = "Successfully added rewards!"
                context['modal_color'] = "col col-lg-12 alert alert-success"

        if request.method == 'POST' and not form.is_valid():
            customer_form = CustomerForm(request.POST)

            if customer_form.is_valid():
                email_address = customer_form.cleaned_data['email']

                get_customer = self.rewards_service_client.get_customers(email_address)
                context['table_2_visibility'] = "visible"
                context['table_1_visibility'] = "invisible"
                context['customer_reward'] = get_customer
                context['message'] = "Successfully search for customer rewards!"
                context['modal_color'] = "col col-lg-12 alert alert-success"

        if request.method == 'POST' and not form.is_valid() and not customer_form.is_valid():
            context['message'] = "Form is invalid, please try again"
            context['modal_color'] = "col col-lg-12 alert alert-danger"

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        context['form'] = form
        context['customer_form'] = customer_form

        return render(request, self.template_name, context)
