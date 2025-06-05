from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class UpdateStore(APIView):
    def put(self, request):
        ...

class CreateAdmin(APIView):
    def post(self, request):
        ...

class DeleteAdmin(APIView):
    def delete(self, request):
        ...