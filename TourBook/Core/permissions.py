from rest_framework import permissions
from django.contrib.auth import get_user_model
from .models.user import Role
from Tour_Organizer.models.tour import Tour
from Tour_Organizer.models.tour_organizer import TourOrganizer
from Client.models.client_request import ClientRequest


from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()

# =================== don't forget to break this file into file for each app [clientPermission => Client , OrganizerPermission => Organzier .....]


class IsSuperAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            return request.user.role == Role.SUPER_ADMIN


class IsAdvertiser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            return request.user.role == Role.ADVERTISER
