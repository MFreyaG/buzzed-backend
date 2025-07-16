from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("account.urls")),
    path("core/", include("core.urls")),
    path("users/", include("user.urls")),
    path("stores/", include("store.urls")),
    path("drinks/", include("drink.urls")),
    path("posts/", include("post.urls")),
]
