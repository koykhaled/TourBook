from Tour_Organizer.models.tour import Tour
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..services.ReactionService import ReactionService

from django.core import exceptions

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    create_reaction=extend_schema(
        summary="add Reaction for Tour", tags=['Tour Reaction']
    )
)
class ReactionView(viewsets.ModelViewSet):
    @action(detail=True)
    def create_reaction(self, request, tour_id):
        try:
            tour = Tour.objects.get(pk=tour_id)
            user = request.user
            message = ""
            ReactionService.validate_reaction(request.data['reaction'])
            check_reaction = ReactionService.check_existing_reaction(user)
            if check_reaction.exists():
                reaction = check_reaction.get()

                message = ReactionService.update_or_delete_reaction(
                    reaction, request.data['reaction'])
            else:
                message = ReactionService.create_reaction(
                    tour, request.data['reaction'], user)
            return Response({'message': message}, status=status.HTTP_200_OK)

        except (exceptions.ValidationError) as e:
            return Response({
                'errors': e
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except TypeError as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour dose not exist!!"
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
