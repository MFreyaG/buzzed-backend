from rest_framework import serializers

from core.serializer import AddressSerializer
from store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    
    class Meta:
        model = Store
        fields = ["id", "name", "description", "icon_url", "address"]
