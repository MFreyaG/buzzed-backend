from django.urls import path

from user.views import ContactView, UserDetailView

urlpatterns = [
    path("<uuid:user_id>", UserDetailView.as_view(), name="user-detail"),
    path("contacts/", ContactView.as_view(), name="user-contacts"),
]
