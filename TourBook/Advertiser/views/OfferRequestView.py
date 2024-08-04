from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ..serializers.OfferRequestSerializer import OfferRequestSerializer
from ..models.offers import Offer

from django.core import exceptions

from drf_spectacular.utils import extend_schema, extend_schema_view


from django_filters.rest_framework import DjangoFilterBackend


from ..services.FilterServices import OfferRequestFilterService


@extend_schema_view(
    get_offer_requests=extend_schema(
        summary="Get Authenticated Advertiser Offers", tags=['Offer Request']),
    handel_offer_requests=extend_schema(
        summary="Accept or Reject an Offer Request", tags=['Offer Request']),
)
class OfferRequestView(viewsets.ModelViewSet):
    serializer_class = OfferRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferRequestFilterService

    def get_queryset(self, offer_id):
        offer = Offer.objects.filter(
            pk=offer_id).prefetch_related('offer_requests').get()

        return offer.offer_requests.all()

    @action(detail=False)
    def get_offer_requests(self, request, offer_id):
        try:
            queryset = self.get_queryset(offer_id)
            queryset = self.filter_queryset(queryset)

            serializer = self.serializer_class(queryset, many=True)
            return Response(
                {
                    'data': serializer.data,
                    'message': "Get Offer requests".title()
                },
                status=status.HTTP_200_OK
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_400_BAD_REQUEST
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

    @action(detail=False)
    def handel_offer_requests(self, request, offer_id, offer_request_id):
        try:
            offer = Offer.objects.filter(
                pk=offer_id).prefetch_related('offer_requests').get()
            offer_request = offer.offer_requests.get(pk=offer_request_id)
            data = {
                "status": request.data['status']
            }
            serializer = self.serializer_class(
                offer_request, data=data, partial=True)
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': "Offer Updated Successfully"
                },
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )

        except (exceptions.ValidationError, TypeError) as e:
            return Response({
                'errors': serializer.errors or e
            },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
