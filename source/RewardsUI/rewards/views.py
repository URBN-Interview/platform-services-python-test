import logging
from django.utils.http import urlencode
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from rewards.forms import AddRewardsForm
from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    """
    A view to manage rewards and customer data.
    """

    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        """
        Initialize the RewardsView.

        Args:
        - logger: Logger object for logging messages.
        - rewards_service_client: Client object to interact with rewards service.
        """
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.

        Retrieves rewards and customer rewards data and renders the template.
        """
        context = self.get_context_data(**kwargs)

        # Retrieve rewards data and customer rewards data
        rewards_data = self.rewards_service_client.get_rewards()
        email = request.GET.get("email", "")
        customers_data = self.rewards_service_client.get_customer_rewards(email=email)

        # Add data to context and render template
        context['customers_data'] = customers_data
        context['rewards_data'] = rewards_data
        return TemplateResponse(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        If 'user_email' is provided, redirect to the same view with email as a query parameter.
        If form data is provided, validate and add order data.
        """
        email = request.POST.get("user_email")
        if email:
            # If email is provided, redirect to the same view with email as a query parameter
            parameters = urlencode({"email": email})
            return redirect("{}?{}".format(reverse("rewards"), parameters))

        # Process AddRewardsForm
        form = AddRewardsForm(request.POST)
        if form.is_valid():
            # If form is valid, add order data and redirect to the same view
            data = {
                "emailId": form.cleaned_data["email"],
                "orderTotal": form.cleaned_data["total"],
            }
            self.rewards_service_client.add_order(data)

        # Redirect back to the same view
        return redirect(reverse("rewards"))

