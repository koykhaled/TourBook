from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .service import create_user_with_role
from djoser.views import UserViewSet
from django.db import transaction


class RegisterView(UserViewSet):
    """View class for user registration.

    Extends the UserViewSet from Djoser and provides registration functionality.

    Attributes:
        serializer_class (UserRegisterSerializer): The serializer class used for user registration.
        permission_classes (tuple): The permission classes applied to the view.

    """

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def register(self, request):
        """Register a new user.

        Validates the registration data, creates a new user, assigns a role, and returns a response.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            serializers.ValidationError: If the registration data is invalid.

        Returns:
            Response: The response containing the registration success message.

        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        super().perform_create(serializer)
        create_user_with_role(user)
        return Response({"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
