from rest_framework import permissions
from django.contrib.auth import get_user_model
from ..models.user import Role

from Advertiser.models.advertiser import Advertiser
from Advertiser.models.offers import Offer

from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


class IsAdvertiserOwnerProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.ADVERTISER:
                    return True
        return False


class IsOfferOwnerOrReadOnly(permissions.BasePermission):
    """
    this permission class used to allow only for the owner to performe update or delete in thire objects
    """

    def has_permission(self, request, view):
        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.ADVERTISER:
                    if request.method == "POST":
                        return True
                    try:
                        offer = Offer.objects.get(
                            pk=view.kwargs['offer_id'])
                        return offer.advertiser_object == request.user.advertiser
                    except ObjectDoesNotExist:
                        return True
