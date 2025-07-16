from rest_framework import serializers

from drink.serializer import DrinkReadSerializer
from post.models import Post, PostImage, PostVideo
from user.serializer import UserSerializer


class PostFilterSerializer(serializers.Serializer):
    user = serializers.UUIDField(required=False)
    drink = serializers.UUIDField(required=False)
    created_at = serializers.DateTimeField(required=False)


class PostReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    drink = DrinkReadSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "drink",
            "score",
            "review",
            "created_at",
        ]
        
class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "drink",
            "score",
            "review",
            "created_at",
        ]


class PostImageFilterSerializer(serializers.Serializer):
    post = serializers.UUIDField(required=False)
    
class PostImageReadSerializer(serializers.ModelSerializer):
    post = PostReadSerializer(read_only=True)
    
    class Meta:
        model = PostImage
        fields = ["id", "post", "image_url"]
    
class PostImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "post", "image_url"]
        
class PostVideoFilterSerializer(serializers.Serializer):
    post = serializers.UUIDField(required=False)
    
class PostVideoReadSerializer(serializers.ModelSerializer):
    post = PostReadSerializer(read_only=True)
    
    class Meta:
        model = PostVideo
        fields = ["id", "post", "video_url"]
    
class PostVideoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = ["id", "post", "video_url"]
