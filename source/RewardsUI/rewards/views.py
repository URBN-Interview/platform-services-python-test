import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient, RewardsServiceError


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        search_email = request.GET.get('email', '').strip()
        context['search_email'] = search_email

        try:
            context['rewards_data'] = self.rewards_service_client.get_rewards()
            if search_email:
                context['customers'] = [self.rewards_service_client.get_customer(search_email)]
            else:
                context['customers'] = self.rewards_service_client.get_customers()
        except RewardsServiceError as exc:
            messages.error(request, str(exc))

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip()

        try:
            order_total = float(request.POST.get('order_total', ''))
            self.rewards_service_client.add_order(email, order_total)
            messages.success(request, 'Order added for ' + email)
        except ValueError:
            messages.error(request, 'Order total must be a number')
        except RewardsServiceError as exc:
            messages.error(request, str(exc))

        return redirect('rewards')
