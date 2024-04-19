import re
from rest_framework import serializers
from Advertiser.models.advertiser import Advertiser, Situation 
from Core.models.attachment import Attachment
from accounts.serializers import UserSerializer
from rest_framework import serializers
from Advertiser.models.offers import Offer, Offer_Attachments, OfferRequest
from django.db.models import Sum
from Advertiser.models.advertiser import AdvertiserAttachments
from Advertiser.models.service import Service

class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.
    """
    class Meta:
        model = Service
        fields = ['id','service_field']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class OfferAttachmentsSerializer(serializers.ModelSerializer):
    attachment_object = AttachmentSerializer()

    class Meta:
        model = Offer_Attachments
        fields = ['attachment_object']
class OfferRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferRequest
        fields = ['id', 'num_of_seat', 'description']
class OfferSerializer(serializers.ModelSerializer):
    offer_attachments = OfferAttachmentsSerializer(many=True, source='offer_attachments.all')
    offer_requests = OfferRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id','num_of_seat','offer_requests','start_date', 'end_date', 'description', 'price_for_one', 'title', 'service', 'offer_attachments', 'advertiser_object']
class AdvertiserSerializers(serializers.ModelSerializer):
    """
    Serializer for the Advertiser model.
    """
    user =UserSerializer()
    service = ServiceSerializer(many=True)
    offers = OfferSerializer(many=True, read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta :
        model = Advertiser
        fields = ['situation','user','place_capacity','place_name','link','axis_x','axis_y','service','offers','available_seats']
        read_only_fields = ('user', 'available_seats')

    def get_available_seats(self, obj):
        total_quantity = sum(obj_offer.num_of_seat for obj_offer in obj.offers.all())
        offer_requests_quantity = sum(obj_request.num_of_seat for obj_offer in obj.offers.all() for obj_request in obj_offer.offer_requests.all())
        return total_quantity - offer_requests_quantity

    def validate(self, attrs):
        """
        Performs validation on the serializer fields.

        Raises:
        - serializers.ValidationError: If any of the validation conditions fail.
        """

        errors = {}
        if 'axis_x' in attrs and (attrs['axis_x'] < -180 or attrs['axis_x'] > 180):
            errors['axis_x'] = "Axis x must be greater than -180 and less than 180."

        if 'axis_y' in attrs and (attrs['axis_y'] < -180 or attrs['axis_y'] > 180):
            errors['axis_y'] = "Axis y must be greater than -180 and less than 180."

        if 'situation' in attrs and attrs['situation'] not in Situation.getSituationKeys():
            errors['situation'] = f"Situation Must be one of {' ,'.join(Situation.getSituationKeys())}"

        if 'place_capacity' in attrs and attrs['place_capacity'] <= 0:
            errors['place_capacity'] = " place capacity must be greater than zero."
            
        if 'avatar' in attrs:
            allowed_types = ["image/jpeg", "image/png"]
            avatar_errors = {}
            if attrs['avatar'].content_type not in allowed_types:
                avatar_errors['type'] = "Only JPEG and PNG image files are allowed."
            max_size = 5 * 1024 * 1024  # 5MB
            if attrs['avatar'].size > max_size:
                avatar_errors['size'] = "The avatar file size should not exceed 5MB."
            if len(avatar_errors) > 0:
                errors['avatar'] = avatar_errors

        if len(errors) > 0:
            raise serializers.ValidationError(errors)

        return attrs
  
    def get_user(self, obj):
        user = obj.user
        user_serializer = UserSerializer(user)
        return user_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user_data = representation.pop('user')
        user_data = {
            'id': user_data['id'],
            'username': user_data['username'],
            'phone': user_data['phone'],
            'email': user_data['email']
        }
        representation.update(user_data)
        return representation
    
