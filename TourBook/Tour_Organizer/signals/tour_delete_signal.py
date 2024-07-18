from django.dispatch import receiver
from django.db.models.signals import pre_delete
from ..models.tour import Tour
from Core.models.notification import Notification
from Client.models.client import Client
from Advertiser.models.advertiser import Advertiser


@receiver(signal=pre_delete, sender=Tour)
def tour_on_delete(instance, **kwargs):
    """
    Signal handler function to execute when a Tour instance is deleted.

    Args:
        instance: The actual instance being deleted.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """

    clients = get_clients(instance)
    advertisers = get_advertisers(instance)
    users = get_users(advertisers, clients)
    send_notification(f"The Tour {instance.title} has been removed", users)
    delete_offer_requests(instance)


def get_clients(instance):
    """
    Retrieve the Users who have client role associated with a given tour instance.

    Args:
        instance: The tour instance for which to retrieve the clients.

    Returns:
        A list of User objects representing the clients associated with the tour.
    """
    return [
        client.user
        for client in Client.objects.filter(client_requests__tour_object=instance).select_related('user')
    ]


def get_advertisers(instance):
    """
    Retrieve the advertisers who have the tour request in their offers.

    Args:
        instance: The tour instance for to access to offer requests to get advertisers.

    Returns:
        A list of User objects representing the advertisers associated with the tour.
    """
    return [
        advertiser.user
        for advertiser in Advertiser.objects.filter(
            offers__offer_requests__offer_point__tour_object=instance
        ).select_related('user').distinct()
    ]


def get_users(advertisers, clients):
    """
    Concatenate the users who have the advertiser role and the clients who have the client role.
    users who are related with tour.

    Args:
        advertisers: A list of User objects representing the advertisers.
        clients: A list of User objects representing the clients.

    Returns:
        A list of User objects representing the concatenated users.
    """
    users = advertisers + clients
    return users


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


def delete_offer_requests(instance):
    """
    Delete the offer requests associated with a tour instance.

    Args:
        instance: The tour instance for which to delete the offer requests.

    Returns:
        None
    """
    for tour_point in instance.tour_points.all():
        tour_point.offer_request.delete()
