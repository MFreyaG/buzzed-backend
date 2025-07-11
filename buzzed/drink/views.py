from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drink.models import Drink, FavoriteDrink
from drink.serializer import (
    DrinkFilterSerializer,
    DrinkReadSerializer,
    DrinkWriteSerializer,
    FavoriteDrinkFilterSerializer,
    FavoriteDrinkWriteSerializer,
)


class DrinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filter_serializer = DrinkFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        validated_filters = filter_serializer.validated_data

        drinks = Drink.objects.filter(**validated_filters)
        serializer = DrinkReadSerializer(drinks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = DrinkWriteSerializer(data=request.data)
        if serializer.is_valid():
            drink = serializer.save()
            return Response(DrinkWriteSerializer(drink).data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class DrinkDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, drink_pk):
        user = get_object_or_404(Drink, pk=drink_pk)
        serializer = DrinkReadSerializer(user)
        return Response(serializer.data)

    def patch(self, request, drink_pk):
        drink = get_object_or_404(Drink, pk=drink_pk)
        serializer = DrinkReadSerializer(drink, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, drink_pk):
        store = get_object_or_404(Drink, pk=drink_pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteDrinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        filter_serializer = FavoriteDrinkFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        validated_filters = filter_serializer.validated_data

        favorite_drinks = FavoriteDrink.objects.filter(**validated_filters)
        serializer = FavoriteDrinkWriteSerializer(favorite_drinks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = FavoriteDrinkWriteSerializer(data=request.data)
        if serializer.is_valid():
            favorite_drink = serializer.save()
            return Response(
                FavoriteDrinkWriteSerializer(favorite_drink).data,
                status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class FavoriteDrinkDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, favorite_drink_pk):
        favorite_drink = get_object_or_404(FavoriteDrink, pk=favorite_drink_pk)
        favorite_drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
