import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import EmailForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        customers_data = self.rewards_service_client.get_all_customers()

        context["customers_data"] = customers_data
        context['rewards_data'] = rewards_data

        #Upon loading, it will display all customer data
        #If email exists, it will display specific customer, else return error message
        #Empty field will display all data as well
        if(request.method == 'GET'):
            form = EmailForm(request.GET)
            if(form.is_valid()):
                if(form.cleaned_data["email"]):
                    email = form.cleaned_data["email"]
                    customers_data = self.rewards_service_client.get_customers(email)
                    context["customers_data"] = customers_data
                    # Error checks to see if email is found or not
                    if(not customers_data):
                        context["customer_error"] = "Email does not exist"

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
