import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from rewards.forms import SearchForm, OrderForm
from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def _load_customer_rewards(self, context, email=None):
        customer_rewards_data = self.rewards_service_client.get_customer_rewards(email)
        context['customer_rewards_data'] = customer_rewards_data

    def get_context_data(self, **kwargs):
        context = super(RewardsView, self).get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()

        search_form = SearchForm(self.request.POST or None)
        order_form = OrderForm(self.request.POST or None)

        context['rewards_data'] = rewards_data
        context['search_form'] = search_form
        context['order_form'] = order_form

        self._load_customer_rewards(context)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        search_form = context["search_form"]
        order_form = context['order_form']

        if 'add-order' in request.POST and order_form.is_valid():
            data = order_form.cleaned_data
            email = data['email']
            amount = data['amount']

            self.rewards_service_client.add_customer_order(email, amount)
            self._load_customer_rewards(context)

            # Clear search form to show possibly new customer
            context['search_form'] = SearchForm()

        if 'search' in request.POST and search_form.is_valid():
            email = search_form.cleaned_data['email']
            self._load_customer_rewards(context, email)

        context['order_form'] = OrderForm()

        return TemplateResponse(request, self.template_name, context)
