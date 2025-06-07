from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("user.urls.auth_urls")),
    path("user/", include("user.urls.user_urls")),
]
