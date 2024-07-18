from rest_framework import serializers
from ..models.tour_attachment import TourAttachment
from Core.models.attachment import Attachment
from Core.helpers.Base64FileHandler import Base64FileField


class AttachmentSerializer(serializers.ModelSerializer):
    file = Base64FileField()

    class Meta:
        model = Attachment
        fields = ('id', 'file')


class TourAttachmentSerializer(serializers.ModelSerializer):
    attachment = AttachmentSerializer()

    class Meta:
        model = TourAttachment
        fields = ('attachment',)

    def create(self, validated_data):
        attachment_data = validated_data.pop('attachment')
        attachment_serializer = AttachmentSerializer(data=attachment_data)
        attachment_serializer.is_valid(raise_exception=True)
        attachment = attachment_serializer.save()
        tour_attachment = TourAttachment.objects.create(
            attachment=attachment, **validated_data)
        return tour_attachment
