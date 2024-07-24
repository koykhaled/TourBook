from django.db.models.signals import post_delete
from ..models.client_request import ClientRequest
from django.dispatch.dispatcher import receiver
from Core.models.notification import Notification


@receiver(signal=post_delete, sender=ClientRequest)
def client_request_delete_notify(instance, *args, **kwargs):
    message = f"MR.{instance.client_object.user.username} canceled his request  on Tour : {instance.tour_object.title}!!!"
    receiver = instance.tour_object.tour_organizer.user
    Notification.objects.create(
        content=message,
        user=receiver
    )
