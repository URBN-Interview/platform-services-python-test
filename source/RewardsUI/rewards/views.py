import logging
from django.http import Http404

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

#import model to this view and calculate rewards here...?
# from .models import CustomerData

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            rewards_data = self.rewards_service_client.get_rewards()
            context['rewards_data'] = rewards_data
        except self.rewards_service_client.DoesNotExist:
            raise Http404("Data does not exist")

        return TemplateResponse(
            request,
            self.template_name,
            context #{"reward" : {"tier" : xx, "xx" : xxx }}
        )


class AddInfo(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            email = request.POST["email"]
            total = request.POST["total"]
            context["info"] = {"email" : email, "total": total}
            print (email)

        except (KeyError):
            return  TemplateResponse(
                request,
                self.template_name,
                {"error_message": "Submit Error"}
            )

        else:

            return TemplateResponse(
                request,
                self.template_name,
                context
            )