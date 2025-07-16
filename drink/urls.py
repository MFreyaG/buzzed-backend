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
    path("favorite-drink/", FavoriteDrinkView.as_view(), name="favorite-drink"),
    path(
        "favorite-drink/<uuid:favorite_drink_pk>",
        FavoriteDrinkDetailView.as_view(),
        name="favorite-drink-detail",
    ),
]
