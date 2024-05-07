from rest_framework import permissions
from django.contrib.auth import get_user_model
from .models.user import Role
from Tour_Organizer.models.tour import Tour
User = get_user_model()


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.auth:
            return request.user.role == Role.SUPER_ADMIN


class IsAdvertiser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.auth:
            return request.user.role == Role.ADVERTISER


class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.auth:
            return request.user.role == Role.ORGANIZER


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.auth:
            return request.user.role == Role.CLIENT


class IsOrganizerOwnerOrReadOnly(permissions.BasePermission):
    """
    this permission class used to allow only for the owner to performe update or delete in thire objects
    """

    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'POST'):
            return True
        else:
            tour = Tour.objects.get(pk=view.kwargs['tour_id'])
            return tour.tour_organizer == request.user.organizer
