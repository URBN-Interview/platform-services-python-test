import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

from rewards.forms import SearchUserForm
from rewards.forms import AddOrderForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.rewards_data = rewards_service_client.get_rewards()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'GET':
            form = SearchUserForm(request.GET)
            if form.is_valid():
                user_data = self.rewards_service_client.get_user(form.cleaned_data['email_address'])
                context['users_data'] = user_data
                context['rewards_data'] = self.rewards_data
            else:
                self.get_data(context)
        else:
            self.get_data(context)
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            form = AddOrderForm(request.POST)
            if form.is_valid():
                self.rewards_service_client.add_order(form.cleaned_data['email_address_order'],
                                                      form.cleaned_data['order_total'])
                context['order_status'] = "ORDER COMPLETE"
            else:
                context['order_status'] = "ORDER FAILED"
        self.get_data(context)
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def get_data(self, context):
        context['rewards_data'] = self.rewards_data
        context['users_data'] = self.rewards_service_client.get_users()
