from Advertiser.models.advertiser import Advertiser
from Core.models.user import Role
from Client.models.client import Client
from Tour_Organizer.models.tour_organizer import TourOrganizer


def create_user_with_role(user):
    match user.role:
        case Role.ORGANIZER:
            TourOrganizer.objects.create(user=user)
        case Role.ADVERTISER:
            Advertiser.objects.create(user=user)
        case Role.CLIENT:
            Client.objects.create(user=user)
        case _:
            raise ValueError(
                f"Role should be in {' ,'.join(Role.getRoleKeys())}")
