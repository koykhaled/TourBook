from rest_framework import status, viewsets
from rest_framework.response import Response
from ..serializers.CommentSerializer import CommentSerializer
from ..models.comments import Comment
from Core.permissions import IsClient
from Tour_Organizer.models.tour import Tour
from django.core import exceptions


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsClient]

    def get_tour_comments(self, request, tour_id):
        try:
            tour = Tour.objects.prefetch_related(
                'tour_comments').get(pk=tour_id)
            comments = tour.tour_comments.all()
            serializer = self.serializer_class(comments, many=True)
            return Response({
                "data": serializer.data
            })
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError:
            return Response({
                'errors': serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
