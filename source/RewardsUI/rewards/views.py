import logging
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from rewards.clients.rewards_service_client import RewardsServiceClient

class RewardsView(TemplateView):
    """
    View for rendering the Rewards Dashboard template.
    """

    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        """
        Initializes the RewardsView with a logger and a RewardsServiceClient instance.

        Args:
            logger (Logger, optional): Logger instance for logging messages. Defaults to logging.getLogger(__name__).
            rewards_service_client (RewardsServiceClient, optional): Instance of RewardsServiceClient for interacting with the Rewards Service API. Defaults to RewardsServiceClient().
        """
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to the view.

        Retrieves rewards data and customer rewards data based on search_email GET parameter.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            TemplateResponse: Template response object.
        """
        context = self.get_context_data(**kwargs)

        # Retrieve rewards data
        rewards_data = self.rewards_service_client.get_rewards()
        
        # Get the search_email from the request GET parameters
        search_email = request.GET.get('search_email')
        
        # Retrieve customer rewards data based on search_email
        customers_rewards = self.rewards_service_client.get_customers_rewards(search_email)
        
        # Add rewards and customers_rewards data to the context
        context['rewards_data'] = rewards_data
        context['customers_rewards_data'] = customers_rewards

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to the view.

        Submits customer's order data and retrieves rewards data and customer rewards data.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            TemplateResponse: Template response object.
        """
        context = self.get_context_data(**kwargs)

        # Retrieve form data
        email = request.POST.get('email')
        total_amount = request.POST.get('total_amount')

        # Submit customer's order data
        if email and total_amount:
            context['success_message'] = self.rewards_service_client.submit_order(email, total_amount)
        else:
            context['error_message'] = 'Please provide both email address and order total.'

        # Retrieve rewards data
        rewards_data = self.rewards_service_client.get_rewards()
        
        # Get the search_email from the request GET parameters
        search_email = request.GET.get('search_email', None)
        
        # Retrieve customer rewards data based on search_email
        customers_rewards = self.rewards_service_client.get_customers_rewards(search_email)
        
        # Add rewards and customers_rewards data to the context
        context['rewards_data'] = rewards_data
        context['customers_rewards_data'] = customers_rewards

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
