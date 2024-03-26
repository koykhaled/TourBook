from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .service import create_user_with_role
from djoser.views import UserViewSet
from django.db import transaction


class RegisterView(UserViewSet):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def register(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        super().perform_create(serializer)
        user = serializer.save(*args, **kwargs)
        create_user_with_role(user)
        return Response({"message": "User Registerd Successfully"}, status=status.HTTP_201_CREATED)
