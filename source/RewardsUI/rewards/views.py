import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

from rewards.forms import SearchUserForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

class SearchUserView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'GET':
            form = SearchUserForm(request.GET, user=request.user)
            if form.is_valid():
                user_data = self.rewards_service_client.get_user(form.cleaned_data['email_address'])
                context['user_data'] = user_data
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

