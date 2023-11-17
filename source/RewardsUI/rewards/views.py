import logging

from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import UserSearchForm, OrderPostForm


class RewardsView(TemplateView):
    """
    RewardsView handles all view updates
    for the rewards template when interacting
    with the rewardsService backend
    """

    template_name = "index.html"

    # This process made me realize I'm really glad I don't work
    # with frontend on a regular basis. But it was incredibly
    # humbling to try and spin up just the absolute basics.
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

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        post_order_form = OrderPostForm(request.POST)
        context["order_form"] = post_order_form

        if request.method == "POST":
            if post_order_form.is_valid():
                email = post_order_form.cleaned_data.get("order_email")
                total = post_order_form.cleaned_data.get("order_total")
                insert_order = self.rewards_service_client.create_order(email, total)

        return HttpResponseRedirect("/rewards/")
