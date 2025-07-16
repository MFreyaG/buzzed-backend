from rest_framework import serializers

from core.serializer import AddressSerializer
from store.models import Store


class StoreFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    doc_number = serializers.CharField(required=False)
    address__postal_code = serializers.CharField(required=False)

class StoreReadSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Store
        fields = ["id", "name", "description", "icon_url", "address"]

class StoreWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "description", "icon_url", "address", "manager"]
