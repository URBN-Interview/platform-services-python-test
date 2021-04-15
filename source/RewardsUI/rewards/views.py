import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.customer_rewards_client import CustomerRewardsClient
from .forms import NewPurchaseForm, EmailLookupForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), customer_rewards_client=CustomerRewardsClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.customer_rewards_client = customer_rewards_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        context['new_purchase_form'] = NewPurchaseForm()
        context['email_lookup_form'] = EmailLookupForm()
        customer_data = self.customer_rewards_client.get_all()
        context['customer_data'] = customer_data

        if request.GET:
            reqStr = request.GET['email'].replace('%40', '@')
            reqObj = {'email': reqStr}
            customer_data = self.customer_rewards_client.get_one(reqObj)
            context['customer_data'] = customer_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            form = NewPurchaseForm(request.POST)
            if form.is_valid():
                updateObj = {"email": form.cleaned_data['email'],
                             "cost": form.cleaned_data['order']}

                # update database
                self.customer_rewards_client.update_record(updateObj)

                # request updated information -> adding a note to engineering log about this
                rewards_data = self.rewards_service_client.get_rewards()
                context['rewards_data'] = rewards_data
                customer_data = self.customer_rewards_client.get_all()
                context['customer_data'] = customer_data
                context['new_purchase_form'] = NewPurchaseForm()
                context['email_lookup_form'] = EmailLookupForm()

            return TemplateResponse(
                request,
                self.template_name,
                context
            )
