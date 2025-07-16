from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, PostImage, PostVideo
from post.serializer import (
    PostFilterSerializer,
    PostImageFilterSerializer,
    PostImageReadSerializer,
    PostImageWriteSerializer,
    PostReadSerializer,
    PostVideoFilterSerializer,
    PostVideoReadSerializer,
    PostVideoWriteSerializer,
    PostWriteSerializer,
)


class PostView(APIView):
    def get(self, request):
        filter_serializer = PostFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        validated_filters = filter_serializer.validated_data

        posts = Post.objects.filter(**validated_filters)
        serializer = PostReadSerializer(posts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = PostWriteSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(PostWriteSerializer(post).data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def patch(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        serializer = PostWriteSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostImageView(APIView):
    def get(self, request):
        filter_serializer = PostImageFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        validated_filters = filter_serializer.validated_data

        post_image = PostImage.objects.filter(**validated_filters)
        serializer = PostImageReadSerializer(post_image, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = PostImageWriteSerializer(data=request.data)
        if serializer.is_valid():
            post_image = serializer.save()
            return Response(
                PostImageWriteSerializer(post_image).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostImageDetailView(APIView):
    def delete(self, request, post_image_pk):
        post_image = get_object_or_404(PostImage, pk=post_image_pk)
        post_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostVideoView(APIView):
    def get(self, request):
        filter_serializer = PostVideoFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        validated_filters = filter_serializer.validated_data

        post_video = PostVideo.objects.filter(**validated_filters)
        serializer = PostVideoReadSerializer(post_video, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = PostVideoWriteSerializer(data=request.data)
        if serializer.is_valid():
            post_video = serializer.save()
            return Response(
                PostVideoWriteSerializer(post_video).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostVideoDetailView(APIView):
    def delete(self, request, post_video_pk):
        post_video = get_object_or_404(PostVideo, pk=post_video_pk)
        post_video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
