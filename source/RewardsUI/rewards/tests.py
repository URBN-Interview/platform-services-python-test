from django.test import TestCase
from unittest.mock import patch, MagicMock
from .views import RewardsView
# Create your tests here.


    
class TestRewardsViewClass(TestCase):

    @patch('pymongo.MongoClient')
    def test_post_success(self, mock_mongo_client):
        mock_collection = MagicMock()
        mock_collection.insert_one.return_value.inserted_id = '123'

        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client = MagicMock()
        mock_client.__getitem__.return_value = mock_db
        mock_mongo_client.return_value = mock_client

        reward_view = RewardsView()

        response = reward_view.post('/^$', {'email': 'sweta@example.com', 'order_total': '2024'})

        # Check response status code
        self.assertEqual(response.status_code, 201)

    @patch('pymongo.MongoClient')
    def test_post_failure(self, mock_mongo_client):
        mock_mongo_client.side_effect = Exception("MongoDB connection error")
        reward_view = RewardsView()

        response = reward_view.post('/^$', {'email': 'sweta@example.com', 'order_total': '2024'})

        # Check response status code
        self.assertEqual(response.status_code, 500)
