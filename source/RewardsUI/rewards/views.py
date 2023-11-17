import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import UserSearchForm, OrderPostForm


class RewardsView(TemplateView):
    template_name = "index.html"

    def __init__(
        self,
        logger=logging.getLogger(__name__),
        rewards_service_client=RewardsServiceClient(),
    ):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    # set initial template contexts
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_all_tiers()
        context["rewards_data"] = rewards_data

        users_data = self.rewards_service_client.get_all_users()
        context["users_data"] = users_data

        # bring in forms and include in context
        user_search_form = UserSearchForm(request.GET)
        context["user_search_form"] = user_search_form

        order_post_form = OrderPostForm(request.GET)
        context["order_post_form"] = order_post_form

        if user_search_form.is_valid():
            email = user_search_form.cleaned_data["user_email"]
            user_data = self.rewards_service_client.get_single_user(email)
            # set context to single user
            context["users_data"] = [user_data]

        return render(request, self.template_name, context)
