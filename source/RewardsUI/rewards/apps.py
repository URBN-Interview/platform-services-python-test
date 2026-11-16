# Django app configuration for the rewards app.

from django.apps import AppConfig


class RewardsuiConfig(AppConfig):
    """App config for the dashboard app. Note: `name` says 'rewardsui' but the
    package is `rewards`; it is unused today since the app is not listed in
    INSTALLED_APPS.
    """

    name = 'rewardsui'
