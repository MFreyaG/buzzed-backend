from rest_framework import serializers

from store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["name", "description", "icon_url"]

    def to_representation(self, instance):
        return {
            "name": instance.name,
            "description": instance.description,
            "icon_url": instance.icon_url,
        }
