from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Address
from core.serializer import AddressSerializer
from user.models import User


class AddressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddressSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            address = serializer.save()
            return Response(
                AddressSerializer(address).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, address_pk):
        address = get_object_or_404(Address, pk=address_pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, address_pk):
        address = get_object_or_404(Address, pk=address_pk)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
