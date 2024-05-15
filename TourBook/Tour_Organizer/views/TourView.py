from rest_framework import viewsets, status
from rest_framework.response import Response


from Core.permissions import IsOrganizer, IsOrganizerOwnerOrReadOnly
from ..serializers.TourSerializer import TourSerializer
from Client.serializers.ClientRequestserializer import ClientRequestSerializer
from Client.models.client_request import ClientRequest
from Client.models.client_request import SituationChoices

from ..signals.handle_tour_request import handel_tour_request
from django.db.models.signals import pre_save

from ..models.tour import Tour

from django.core import exceptions
from datetime import datetime


class TourView(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    permission_classes = [IsOrganizer, IsOrganizerOwnerOrReadOnly]

    def get_organizer_tours(self, request):
        try:
            tour_organizer = request.user.organizer
            tours = Tour.objects.filter(
                tour_organizer=tour_organizer).prefetch_related('tour_organizer')
            serializer = self.serializer_class(tours, many=True)

            return Response(
                {
                    'data': serializer.data,
                    'message': "retrive organizer tours done".title()
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_other_organizers_tours(self, request):
        try:
            tour_organizer = request.user.organizer
            tours = Tour.objects.exclude(
                tour_organizer=tour_organizer).prefetch_related('tour_organizer')
            serializer = self.serializer_class(tours, many=True)
            return Response(
                {
                    'data': serializer.data,
                    'message': "retrive other organizers tours done".title()
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_tour(self, request, tour_id):
        try:
            tour = Tour.objects.filter(
                pk=tour_id).prefetch_related('tour_organizer').get()
            serializer = self.serializer_class(tour)
            return Response(
                {
                    'data': serializer.data,
                    'message': "retrive tour done".title()
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        try:
            tour_organizer = request.user.organizer
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(tour_organizer=tour_organizer)
            return Response(
                {
                    'data': serializer.data,
                    'message': "Tour Created Successfully"
                },
                status=status.HTTP_201_CREATED
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour dose not exist!!"
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception:
            return Response({
                'errors': serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )

    def update_tour(self, request, tour_id):
        try:
            tour = Tour.objects.get(pk=tour_id)
            serializer = self.serializer_class(
                tour, data=request.data, partial=True)
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            else:
                serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': "Tour Updated Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
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

    def delete(self, request, tour_id):
        try:
            tour = Tour.objects.get(pk=tour_id)
            tour.delete()
            return Response(
                {
                    'message': "Tour Deleted Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post_tour(self, request, tour_id):
        try:
            tour = Tour.objects.get(pk=tour_id)

            serializer = self.serializer_class(
                tour, data={'posted': True, 'posted_at': datetime.now()}, partial=True)

            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            else:
                serializer.save()

            return Response(
                {
                    'message': "Tour Posted Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError as e:
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

    def get_tour_requests(self, request, tour_id):
        try:
            tour = Tour.objects.prefetch_related(
                'tour_requests').get(pk=tour_id)
            tour_requests = tour.tour_requests.filter(
                situation=SituationChoices.WAITING)
            serializer = ClientRequestSerializer(tour_requests, many=True)
            return Response(
                {
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
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

    def handel_request(self, request, tour_id):
        try:
            tour = Tour.objects.prefetch_related(
                'tour_requests').get(pk=tour_id)
            tour_request = tour.tour_requests.get(pk=request.data['id'])
            request_serializer = ClientRequestSerializer(
                tour_request, data={"situation": request.data['situation']}, partial=True)
            if not request_serializer.is_valid():
                raise exceptions.ValidationError(request_serializer.errors)
            request_serializer.save()
            message = ""
            if request_serializer.data['situation'] == SituationChoices.ACCEPTED:
                message = "Your Request Accepted"
            elif request_serializer.data['situation'] == SituationChoices.REJECTED:
                message = "Your Request Regected"

            return Response(
                {
                    "message": message
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError:
            return Response({
                'errors': request_serializer.errors
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
