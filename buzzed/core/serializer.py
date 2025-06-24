from rest_framework import serializers

from core.models import Address
from user.models import User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "country",
            "state",
            "city",
            "neighborhood",
            "street",
            "number",
            "complement",
            "postal_code",
        )

    def create(self, validated_data):
        address = Address.objects.create(**validated_data)

        user_id = self.context["request"].user.id
        user = User.objects.get(pk=user_id)
        user.address = address
        user.save()

        return address
