from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("auth.urls")),
    path("core/", include("core.urls.core_urls")),
    path("user/", include("user.urls")),
]
