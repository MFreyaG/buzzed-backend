from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from store.models import Store
from store.serializer import StoreSerializer


class StoreView(APIView):
    def get(self, request): ...
    
    def post(self, request): ...