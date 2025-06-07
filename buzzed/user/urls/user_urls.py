from django.urls import path

from user.views import ContactView, UserView

urlpatterns = [
    path("<int:user_pk>", UserView.as_view(), name="user"),
    path("contacts/", ContactView.as_view(), name="user-contacts"),
]
