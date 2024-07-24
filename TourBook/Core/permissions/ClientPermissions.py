from rest_framework import permissions
from django.contrib.auth import get_user_model
from ..models.user import Role
from Client.models.client import Client
from Client.models.client_request import ClientRequest
from Client.models.comments import Comment

from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()


class IsClientOwnerProfile(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.CLIENT:
                    if request.method == "POST":
                        return True
                    try:
                        client = Client.objects.get(
                            pk=view.kwargs['client_id'])
                        return client == request.user.client
                    except ObjectDoesNotExist:
                        return True


class IsRequestOwnerOrReadOnly(permissions.BasePermission):
    """
    this permission class used to allow only for the owner to performe update or delete in thire objects
    """

    def has_permission(self, request, view):
        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.CLIENT:
                    if request.method == "POST":
                        return True
                    try:
                        client_request = ClientRequest.objects.get(
                            pk=view.kwargs['request_id'])
                        return client_request.client_object == request.user.client
                    except ObjectDoesNotExist:
                        return True


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    this permission class used to allow only for the owner to performe update or delete in thire objects
    """

    def has_permission(self, request, view):
        if request.auth:
            if request.method in ('GET', 'HEAD', 'OPTIONS'):
                return True
            else:
                if request.user.role == Role.CLIENT:
                    if request.method == "POST":
                        return True
                    try:
                        comment = Comment.objects.get(
                            pk=view.kwargs['comment_id'])
                        return comment.client_object == request.user.client
                    except ObjectDoesNotExist:
                        return True
