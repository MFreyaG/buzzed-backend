from django.urls import path

from store.views import StoreView

urlpatterns = [path("<int:store:pk>/", StoreView.as_view(), name="store")]
