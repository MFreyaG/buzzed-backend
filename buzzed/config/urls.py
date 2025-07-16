from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("account.urls")),
    path("core/", include("core.urls")),
    path("user/", include("user.urls")),
    path("store/", include("store.urls")),
    path("drink/", include("drink.urls")),
    path("post/", include("post.urls")),
]
