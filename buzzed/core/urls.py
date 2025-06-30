from django.urls import path

from core.views import AddressDetailView, AddressView

urlpatterns = [
    path("address/", AddressView.as_view(), name="address"),
    path(
        "address/<uuid:address_pk>/", AddressDetailView.as_view(), name="address-detail"
    ),
]
