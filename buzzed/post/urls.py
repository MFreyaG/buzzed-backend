from django.urls import path

from post.views import (
    PostDetailView,
    PostImageDetailView,
    PostImageView,
    PostVideoDetailView,
    PostVideoView,
    PostView,
)

urlpatterns = [
    path("post/", PostView.as_view(), name="post"),
    path("post/<uuid:post_pk>", PostDetailView.as_view(), name="post-detail"),
    path("post-image", PostImageView.as_view(), name="post-image"),
    path("post-video", PostVideoView.as_view(), name="post-video"),
    path(
        "post-image/<uuid:post_image_pk>",
        PostImageDetailView.as_view(),
        name="post-image-detail",
    ),
    path(
        "post-video/<uuid:post_video_pk>",
        PostVideoDetailView.as_view(),
        name="post-video-detail",
    ),
]
