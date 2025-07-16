from django.urls import path

from drink.views import (
    DrinkDetailView,
    DrinkView,
    FavoriteDrinkDetailView,
    FavoriteDrinkView,
)

urlpatterns = [
    path("", DrinkView.as_view(), name="drink"),
    path("<uuid:drink_pk>", DrinkDetailView.as_view(), name="drink-detail"),
    path("favorite-drinks/", FavoriteDrinkView.as_view(), name="favorite-drink"),
    path(
        "favorite-drinks/<uuid:favorite_drink_pk>",
        FavoriteDrinkDetailView.as_view(),
        name="favorite-drink-detail",
    ),
]
