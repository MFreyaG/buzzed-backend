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
        user = User.objects.get(id=user_id)
        user.address = address
        user.save()

        return address

    def to_representation(self, instance):
        return {
            "country": instance.country,
            "state": instance.state,
            "city": instance.city,
            "neighborhood": instance.neighborhood,
            "street": instance.street,
            "number": instance.number,
            "complement": instance.complement,
            "postal_code": instance.postal_code,
        }
