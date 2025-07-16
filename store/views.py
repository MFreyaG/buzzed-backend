from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from store.models import Store
from store.permissions import IsManagerOrAdmin
from store.serializer import StoreReadSerializer, StoreWriteSerializer, StoreFilterSerializer


class StoreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filter_serializer = StoreFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        validated_filters = filter_serializer.validated_data

        stores = Store.objects.filter(**validated_filters)
        serializer = StoreReadSerializer(stores, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = StoreWriteSerializer(data=request.data)
        if serializer.is_valid():
            store = serializer.save()
            return Response(StoreWriteSerializer(store).data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class StoreDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

    def get(self, request, store_pk):
        store = get_object_or_404(Store, pk=store_pk)
        serializer = StoreReadSerializer(store)
        return Response(serializer.data)

    def patch(self, request, store_pk):
        store = get_object_or_404(Store, pk=store_pk)
        self.check_object_permissions(request, store)
        serializer = StoreReadSerializer(
            store, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, store_pk):
        store = get_object_or_404(Store, pk=store_pk)
        self.check_object_permissions(request, store)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
