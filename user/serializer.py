from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from user.models import Contact, User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "icon_url"]
        read_only_fields = ["id"]


class ContactSerializer(serializers.Serializer):
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        follower = self.context["request"].user
        followed = validated_data["followed"]

        contact = Contact.objects.create(follower=follower, followed=followed)
        contact.full_clean()
        contact.save()
        return contact

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "follower": instance.follower.id,
            "followed": instance.followed.id,
        }
