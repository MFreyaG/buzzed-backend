from rest_framework import serializers

from core.models import Address
from user.models import User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "country",
            "state",
            "city",
            "neighborhood",
            "street",
            "number",
            "complement",
            "postal_code",
        )
