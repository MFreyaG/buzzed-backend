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
    user2 = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        user1 = self.context["request"].user
        user2 = validated_data["user2"]

        contact = Contact.objects.create(user1=user1, user2=user2)
        contact.full_clean()
        contact.save()
        return contact

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "follower": instance.user1.id,
            "followed": instance.user2.id,
        }
