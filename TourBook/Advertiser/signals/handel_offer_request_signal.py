from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from ..models.offers import OfferRequest, Status
from Core.models.notification import Notification


@receiver(signal=post_save, sender=OfferRequest)
def handel_offer_requests(instance, *args, **kwargs):
    if instance.status != Status.WAITING:
        if instance.status == Status.ACCEPTED:
            offer = instance.offer_object
            offer.num_of_seat = offer.num_of_seat - instance.num_of_seat
            offer.save()
            message = f"The Advertiser : {instance.offer_object.advertiser_object.user.username} has accepted your request for the offer : {instance.offer_object.title}"
        elif instance.status == Status.REJECTED:
            message = f"The Advertiser : {instance.offer_object.advertiser_object.user.username} has regected your request for the offer : {instance.offer_object.title}"
        Notification.objects.create(
            content=message,
            user=instance.offer_point.tour_object.tour_organizer.user
        )
