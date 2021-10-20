import logging

from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.forms import SubmitOrderForm, SearchUserForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email_address = request.GET.get('email_address')  # search by email
        context['rewards_data'] = self.rewards_service_client.get_user_rewards(email_address)
        context['tiers_data'] = self.rewards_service_client.get_tiers()
        context['submit_order_form'] = SubmitOrderForm()
        context['search_user_form'] = SearchUserForm()
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email_address = request.POST.get('email_address')
        order_total = request.POST.get('order_total')
        form = SubmitOrderForm(request.POST)
        if form.is_valid():
            try:
                self.rewards_service_client.post_reward(email_address, order_total)
            except ValidationError as e:
                if 'email' in e.args[0]:
                    form.add_error('email_address', e.args[0])
                elif 'order' in e.args[0].lower():
                    form.add_error('order_total', e.args[0])
        context['rewards_data'] = self.rewards_service_client.get_user_rewards(email_address)
        context['tiers_data'] = self.rewards_service_client.get_tiers()
        context['submit_order_form'] = SubmitOrderForm()
        context['search_user_form'] = SearchUserForm()
        context['errors'] = form.errors
        return TemplateResponse(
            request,
            self.template_name,
            context
        )
