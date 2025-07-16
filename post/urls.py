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
    path("", PostView.as_view(), name="post"),
    path("<uuid:post_pk>", PostDetailView.as_view(), name="post-detail"),
    path("post-images", PostImageView.as_view(), name="post-image"),
    path("post-videos", PostVideoView.as_view(), name="post-video"),
    path(
        "post-images/<uuid:post_image_pk>",
        PostImageDetailView.as_view(),
        name="post-image-detail",
    ),
    path(
        "post-videos/<uuid:post_video_pk>",
        PostVideoDetailView.as_view(),
        name="post-video-detail",
    ),
]
