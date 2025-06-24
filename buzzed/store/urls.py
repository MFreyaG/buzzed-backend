from django.urls import path

from store.views import StoreView, StoreDetailView

urlpatterns = [
    path("", StoreView.as_view(), name="store"),
    path("<uuid:store_pk>/", StoreDetailView.as_view(), name="store-detail"),
]
