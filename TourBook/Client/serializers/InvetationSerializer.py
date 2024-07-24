from rest_framework import serializers
from Tour_Organizer.models.tour import Tour
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class InvetationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    tour_url = serializers.URLField()

    def create(self, validated_data):
        tour = Tour.objects.get(pk=self.context['tour_id'])
        sender = self.context['request'].user
        receiver = validated_data['email']
        tour_url = validated_data['tour_url']

        context = {
            'tour_url': tour_url,
            'sender_name': sender.username,
        }
        html_context = render_to_string('email/invetation.html', context)

        email_message = EmailMessage(
            subject=f"You're invited to a {tour.title} in Tour Book!",
            body=html_context,
            from_email=sender.email,
            to=[receiver]
        )
        email_message.content_subtype = 'html'
        email_message.send()

        return {'email': receiver, 'tour_url': tour_url}
