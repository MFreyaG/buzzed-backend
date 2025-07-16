from django.urls import path

from core.views import AddressDetailView, AddressView

urlpatterns = [
    path("addresses/", AddressView.as_view(), name="address"),
    path(
        "addresses/<uuid:address_pk>",
        AddressDetailView.as_view(),
        name="address-detail",
    ),
]
