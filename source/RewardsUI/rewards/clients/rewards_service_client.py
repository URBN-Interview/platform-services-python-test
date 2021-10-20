import requests
import logging

from django.core.exceptions import ValidationError
from requests import HTTPError

log = logging.getLogger(__name__)


class RewardsServiceClient:

    def __init__(self):
        self.root = 'http://rewardsservice:7050'
        self.rewards_url = self.root + '/rewards'
        self.tiers_url = self.root + '/tiers'

    def get_rewards(self):
        log.info('Getting rewards')
        try:
            response = requests.get(self.rewards_url)
            response.raise_for_status()
            return response.json().get('rewards', [])
        except HTTPError as e:
            log.exception('Error raised when requesting rewards, %r', str(e))
            return []

    def get_user_rewards(self, email):
        log.info('Getting rewards for user: %r', email)
        if not email:
            return self.get_rewards()
        try:
            response = requests.get(self.rewards_url, params={'email': email})
            response.raise_for_status()
            return [response.json()]
        except HTTPError as e:
            log.exception('Error raised when requesting rewards for user: %r, %r', email, str(e))
            return []

    def post_reward(self, email, order_total):
        response = requests.post(self.rewards_url, params={'email': email}, json={'order_total': order_total})
        try:
            response.raise_for_status()
            return response.json().get('rewards')
        except HTTPError as e:
            log.exception('Error raised when submitting rewards for user: %r, %r', email, str(e))
            raise ValidationError(response.json().get('message', 'Unknown error'))

    def get_tiers(self):
        try:
            response = requests.get(self.tiers_url)
            response.raise_for_status()
            return response.json().get('tiers', [])
        except HTTPError as e:
            log.exception('Error raised when getting reward tiers, %r', str(e))
            return []
