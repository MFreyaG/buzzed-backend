from django.urls import path

from store.views import StoreDetailView, StoreView

urlpatterns = [
    path("", StoreView.as_view(), name="store"),
    path("<uuid:store_pk>/", StoreDetailView.as_view(), name="store-detail"),
]
