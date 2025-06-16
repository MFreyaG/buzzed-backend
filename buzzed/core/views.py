from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializer import AddressSerializer
from user.models import User


class AddressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.address:
            return Response(
                {"detail": "User has already created an address"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AddressSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            address = serializer.save()
            return Response(
                AddressSerializer(address).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors)

    def put(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        address = user.address
        serializer = AddressSerializer(
            address, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
