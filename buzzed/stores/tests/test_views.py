import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

class StoreTestCase(TestCase):
    fixtures = ['user.json']
    
    def setUp(self):
        self.client = Client()
    
    def test_update_store(self):
        valid_store_data = {
            "name":"TestStore",
            "doc_number":"11235813213455",
            "description": "TestStore description",
            "manager": "testuser@email.com",
            "icon_url": "https://example.com/icon.jpg"
        }
        response = self.client.post(
            reverse('create-store'),
            data=json.dumps(valid_store_data),
            content_type='application/json'
        )