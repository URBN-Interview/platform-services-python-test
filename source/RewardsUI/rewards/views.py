import logging
# from django.http import Http404

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient, AddedOrders, GetAllInfo

#import model
from models import OrderData

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
            context #{"reward" : {"tier" : xx, "xx" : xxx }}
        )


class AddInfo(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=AddedOrders()):
        self.logger = logger

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            email = request.POST["email"]
            total = request.POST["total"]
            context["info"] = {"email" : email, "total": total}

        except (KeyError):
            return  TemplateResponse(
                request,
                self.template_name,
                {"error_message": "Submit Error"}
            )

        else:
            entry = OrderData(Email_Address = email, Order_Total = total)
            entry.save()

            return TemplateResponse(
                request,
                self.template_name,
                context
            )

class UserRewards(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=GetAllInfo()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        all_info = self.rewards_service_client.get_all_info()
        context['all info'] = all_info

        return TemplateResponse(
            request,
            self.template_name,
            context
        )