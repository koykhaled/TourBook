from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from Client.models.client_request import ClientRequest, SituationChoices
from Core.models.notification import Notification


@receiver(signal=pre_save, sender=ClientRequest)
def handel_tour_request(instance, *args, **kwargs):
    if instance.situation != SituationChoices.WAITING:
        if instance.situation == SituationChoices.ACCEPTED:
            tour = instance.tour_object
            tour.seat_num = tour.seat_num - instance.seat_num
            tour.save()
            message = f"The organizer : {instance.tour_object.tour_organizer.user.username} has accepted your request for the trip : {instance.tour_object.title}"
        elif instance.situation == SituationChoices.REJECTED:
            message = f"The organizer : {instance.tour_object.tour_organizer.user.username} has regected your request for the trip : {instance.tour_object.title}"

        Notification.objects.create(
            content=message,
            user=instance.client_object.user
        )
