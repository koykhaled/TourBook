from rest_framework import serializers

from Advertiser.models.service import Service


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.
    """
    class Meta:
        model = Service
        fields = ['id', 'service_field']
