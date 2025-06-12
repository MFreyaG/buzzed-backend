import json

from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from store.models import Store
from user.models import User

class StoreTestCase(APITestCase):
    fixtures = ["stores.json"]
    
    def setUp(self):
        ...