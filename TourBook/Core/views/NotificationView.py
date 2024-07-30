from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from ..serializer.NotificationSerializer import NotificationSerializer


@extend_schema_view(
    get_notifications=extend_schema(
        summary="Get Notifications for the Authenticated User", tags=['Notification'])
)
class NotificationView(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    @action(detail=False)
    def get_notifications(self, request):
        try:
            user = request.user
            notifications = user.notifications.order_by('-created_at')[:5]

            serializer = self.serializer_class(notifications, many=True)
            return Response(
                {
                    'data': serializer.data,
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
