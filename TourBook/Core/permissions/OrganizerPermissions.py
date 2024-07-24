from rest_framework import permissions
from django.contrib.auth import get_user_model
from ..models.user import Role
from Tour_Organizer.models.tour import Tour
from Tour_Organizer.models.tour_organizer import TourOrganizer


from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


class IsOrganizerOwnerProfile(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.ORGANIZER:
                    if request.method == "POST":
                        return True
                    try:
                        organizer = TourOrganizer.objects.get(
                            pk=view.kwargs['id'])
                        print(organizer == request.user.organizer)
                        return organizer == request.user.organizer
                    except ObjectDoesNotExist:
                        return True


class IsTourOwnerOrReadOnly(permissions.BasePermission):
    """
    this permission class used to allow only for the owner to performe update or delete in thire objects
    """

    def has_permission(self, request, view):
        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.ORGANIZER:
                    if request.method == "POST":
                        return True
                    try:
                        tour = Tour.objects.get(pk=view.kwargs['tour_id'])
                        return tour.tour_organizer == request.user.organizer
                    except ObjectDoesNotExist:
                        return True
