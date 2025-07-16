from rest_framework import serializers

from drink.models import Drink, FavoriteDrink, Ingredient
from store.serializer import StoreReadSerializer
from user.serializer import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class DrinkFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    price = serializers.CharField(required=False)
    store_name = serializers.CharField(required=False)
    store = serializers.UUIDField(required=False)


class DrinkReadSerializer(serializers.ModelSerializer):
    store = StoreReadSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Drink
        fields = [
            "id",
            "name",
            "store",
            "store_name",
            "description",
            "price",
            "alcohol_percentage",
            "image_url",
            "ingredients",
        ]


class DrinkWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = [
            "id",
            "name",
            "store",
            "store_name",
            "description",
            "price",
            "alcohol_percentage",
            "image_url",
            "ingredients",
        ]


class FavoriteDrinkFilterSerializer(serializers.Serializer):
    user = serializers.UUIDField(required=False)
    drink = serializers.UUIDField(required=False)


class FavoriteDrinkReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    drink = DrinkReadSerializer(read_only=True)

    class Meta:
        model = FavoriteDrink
        fields = ["id", "drink", "user"]


class FavoriteDrinkWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteDrink
        fields = ["id", "drink", "user"]
