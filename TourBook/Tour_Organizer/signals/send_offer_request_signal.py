from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from ..models.tour import Tour
from Core.models.notification import Notification


@receiver(signal=post_save, sender=Tour)
def send_notification_on_request(instance, *args, **kwargs):

    tour_points = instance.tour_points.all()
    print("khaled")
    offer_rquests = [
        tour_point.offer_request
        for tour_point in tour_points
    ]
    message = f"The Organizer : {instance.tour_organizer.user.username} request to join your Offer,He is waiting for your response"
    advertisers = set(
        offer_request.offer_object.advertiser_object.user
        for offer_request in offer_rquests
    )

    send_notification(message, list(advertisers))


def send_notification(message, users):
    """
    Send a notification message to a list of users.

    Args:
        message: The content of the notification message.
        users: A list of User objects representing the recipients of the notification.

    Returns:
        None
    """
    notifications = [
        Notification(content=message, user=user)
        for user in users
    ]
    Notification.objects.bulk_create(notifications)
