from django.urls import path
from stores.views import CreateStore, UpdateStore

urlpatterns = [
    path('<int:pk>/update-store', UpdateStore.as_view(), name='update_store')
]