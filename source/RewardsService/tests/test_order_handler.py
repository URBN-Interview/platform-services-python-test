import pytest
import json
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from motor.motor_tornado import MotorClient
from pymongo.errors import PyMongoError

from source.RewardsService.rewardsservice.handlers.order_handler import OrderHandler


class TestOrderHandler(AsyncHTTPTestCase):
    """
    Created pytest for Order handler. Note, it is Not functional.
    """
    def get_app(self):
        db = MotorClient()['Rewards']
        return Application([(r'/order', OrderHandler, dict(db=db))])

    @pytest.mark.gen_test
    async def test_valid_order(self):
        # Test a valid order
        data = {'email': 'test@example.com', 'total': 100}
        response = await self.fetch('/order', method='POST', body=json.dumps(data))
        assert response.code == 200
        response_data = json.loads(response.body.decode())
        assert response_data['email'] == data['email']
        assert response_data['points'] == data['total']
        assert response_data['reward_tier'] == 'A'
        assert response_data['reward_tier_name'] == '5% off purchase'
        assert response_data['next_reward_tier'] == 'B'
        assert response_data['next_reward_tier_name'] == '10% off purchase'
        assert response_data['next_reward_tier_progress'] == 0.0

    @pytest.mark.gen_test
    async def test_invalid_order(self):
        # Test an invalid order with missing data
        data = {'email': 'test@example.com'}
        response = await self.fetch('/order', method='POST', body=json.dumps(data))
        assert response.code == 400

    @pytest.mark.gen_test
    async def test_db_error(self, monkeypatch):
        # Test an error when accessing the database
        def mock_insert(*args, **kwargs):
            raise PyMongoError('Database error')
        monkeypatch.setattr('motor.motor_tornado.AsyncIOMotorCollection.insert_one', mock_insert)
        data = {'email': 'test@example.com', 'total': 100}
        response = await self.fetch('/order', method='POST', body=json.dumps(data))
        assert response.code == 500
