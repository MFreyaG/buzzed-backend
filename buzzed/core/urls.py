from django.urls import path

from core.views import AddressView

urlpatterns = [path("address/", AddressView.as_view(), name="address")]
