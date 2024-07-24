from rest_framework import status, viewsets
from rest_framework.response import Response
from ..serializers.CommentSerializer import CommentSerializer
from rest_framework.decorators import action

from Core.permissions.ClientPermissions import IsCommentOwnerOrReadOnly
from Tour_Organizer.models.tour import Tour
from django.core import exceptions
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    get_tour_comments=extend_schema(
        summary="List of All Comments For Specific Tour", tags=['Comments']),
    create_comment=extend_schema(
        summary="Add Comment For a Tour", tags=['Comments']),
    update_comment=extend_schema(
        summary="Update Comment", tags=['Comments']),
    delete_comment=extend_schema(
        summary="Delete Comment", tags=['Comments']),
)
class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwnerOrReadOnly]

    @action(detail=False)
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
                'errors': "Tour Dosen't Exist!!"
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False)
    def create_comment(self, request, tour_id):
        try:
            tour = Tour.objects.prefetch_related(
                'tour_comments').get(pk=tour_id)
            client = request.user.client
            data = {
                'comment': request.data['comment'],
                'tour': tour.id
            }
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            serializer.save(client_object=client)
            return Response({
                "data": serializer.data
            })
        except exceptions.ObjectDoesNotExist as e:
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

    @action(detail=False)
    def update_comment(self, request, tour_id, comment_id):
        try:
            tour = Tour.objects.prefetch_related(
                'tour_comments').get(pk=tour_id)
            comment = tour.tour_comments.get(pk=comment_id)
            serializer = self.serializer_class(
                comment, data=request.data, partial=True)
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            serializer.save()
            return Response({
                "data": "Comment Updated Successfully"
            })
        except exceptions.ObjectDoesNotExist as e:
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

    @action(detail=False)
    def delete_comment(self, request, tour_id, comment_id):
        try:
            tour = Tour.objects.prefetch_related(
                'tour_comments').get(pk=tour_id)
            comment = tour.tour_comments.get(pk=comment_id)
            comment.delete()
            return Response({
                "data": "comment Deleted Successfully"
            })
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
