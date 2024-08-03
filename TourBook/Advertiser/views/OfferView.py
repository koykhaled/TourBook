from rest_framework import status, viewsets
from ..serializers.NewOfferSerializer import OfferSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, extend_schema_view

from django.core import exceptions

from ..models.offers import Offer, Service


@extend_schema_view(
    get_advertiser_offers=extend_schema(
        summary="Get Authenticated Advertiser Offers", description="you need JWT Token to show the offers", tags=['Offers']),
    create_offer=extend_schema(
        summary="create an Offer", tags=['Offers']),
    update_offer=extend_schema(
        summary="Update an Offer", tags=['Offers']),
    get_offer=extend_schema(summary="Retrive an Offer", tags=['Offers']),
)
class OfferView(viewsets.ModelViewSet):
    serializer_class = OfferSerializer

    @action(detail=False)
    def get_advertiser_offers(self, request):
        try:
            advertiser = request.user.advertiser
            offers = Offer.objects.prefetch_related(
                'offer_attachments', 'advertiser_object').filter(advertiser_object=advertiser)

            serializer = self.serializer_class(offers, many=True)
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

    @action(detail=False)
    def get_offer(self, request, offer_id):
        try:
            offer = Offer.objects.filter(
                pk=offer_id).select_related('advertiser_object').get()
            serializer = self.serializer_class(offer)
            return Response(
                {
                    'data': serializer.data,
                    'message': "retrive an offer done".title()
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
    def create_offer(self, request):
        # don't forget to apply image classification
        try:
            advertiser = request.user.advertiser
            serializer = self.serializer_class(data=request.data)
            service = Service.objects.get(pk=request.data['service'])
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)
            serializer.save(advertiser_object=advertiser, service=service)

            return Response(
                {
                    'data': serializer.data,
                    'message': "Offer Created Successfully"
                },
                status=status.HTTP_201_CREATED
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

    @action(detail=False)
    def update_offer(self, request, offer_id):
        try:
            offer = Offer.objects.get(pk=offer_id)
            serializer = self.serializer_class(
                offer, data=request.data, partial=True)
            if not serializer.is_valid():
                raise exceptions.ValidationError(serializer.errors)

            service = Service.objects.get(
                pk=request.data['service']) if 'service' in request.data else None
            serializer.save(service=service)

            return Response(
                {
                    'data': serializer.data,
                    'message': "Offer Updated Successfully"
                },
                status=status.status.HTTP_200_OK
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
