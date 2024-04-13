from rest_framework import permissions
from django.contrib.auth import get_user_model
from .models.user import Role
User = get_user_model()


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.SUPER_ADMIN


class IsAdvertiser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADVERTISER


class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ORGANIZER


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.CLIENT
