from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema_view, extend_schema

from rest_framework.permissions import AllowAny


from Core.permissions import IsTourOwnerOrReadOnly
from ..serializers.TourSerializer import TourSerializer
from Client.serializers.ClientRequestserializer import ClientRequestSerializer
from Client.models.client_request import SituationChoices


from ..models.tour import Tour


from django.core import exceptions
from datetime import datetime


@extend_schema_view(

    list=extend_schema(summary="List all tours", tags=["Tour"]),
    create=extend_schema(summary="Create a new tour", tags=["Tour"]),
    retrieve=extend_schema(summary="Retrieve a tour", tags=["Tour"]),
    update=extend_schema(summary="Update a tour", tags=["Tour"]),
    destroy=extend_schema(summary="Delete a tour", tags=["Tour"]),
    get_organizer_tours=extend_schema(
        summary="Retrieve tours by organizer", tags=["Tour"]),
)
class TourView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [IsTourOwnerOrReadOnly]

    def list(self, request):
        try:
            tours = Tour.objects.prefetch_related(
                'tour_attachments', 'tour_organizer').all()
            page = self.paginate_queryset(tours)

            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(tours, many=True)
            return Response(
                {
                    'data': serializer.data,
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
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

    def retrieve(self, request, tour_id):
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
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
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

    def update(self, request, tour_id):
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

    def destroy(self, request, tour_id):
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


@extend_schema_view(
    get=extend_schema(
        summary="get latest 2 tours for UnAutheticated Users", tags=["HomeTours"]),

)
class UnauthToursView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TourSerializer

    def get(self, request):
        try:
            tours = Tour.objects.prefetch_related(
                'tour_attachments', 'tour_organizer').order_by('posted_at').all()[:2]
            serializer = self.serializer_class(tours, many=True)
            return Response(
                {
                    'data': serializer.data,
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
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


@extend_schema_view(

    list=extend_schema(summary="List all Organizer tours",
                       tags=["Organizer Tours"]),
)
class OrganizerTours(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    permission_classes = [IsTourOwnerOrReadOnly]

    def list(self, request):
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


@extend_schema_view(

    list=extend_schema(summary="List of Others Organizers tours",
                       tags=["Other Organizers Tours"]),
)
class OtherOrganizersTours(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    permission_classes = [IsTourOwnerOrReadOnly]

    def list(self, request):
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

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(

    list=extend_schema(summary="List all tour requests",
                       tags=["Tour Requests"]),
    create=extend_schema(
        summary="accept the request from the client or reject it", tags=["Tour Requests"]),

)
class TourRequests(viewsets.ModelViewSet):
    permission_classes = [IsTourOwnerOrReadOnly]

    def list(self, request, tour_id):
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

    def create(self, request, tour_id):
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


@extend_schema_view(
    create=extend_schema(
        summary="post the tour", tags=["Post Tour"]),
)
class TourPosted(viewsets.ModelViewSet):
    permission_classes = [IsTourOwnerOrReadOnly]
    serializer_class = TourSerializer

    def create(self, request, tour_id):
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
