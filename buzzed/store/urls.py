from django.urls import path

from store.views import StoreView

urlpatterns = [
    path("", StoreView.as_view(), name=...),
    path("<int:store_pk>/", StoreView.as_view(), name="store"),
]
