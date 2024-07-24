from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from rest_framework.viewsets import ModelViewSet

from Advertiser.models.offers import OfferRequest
from ..serializers.TourOrganizerSerializer import TourOrganizerSerializer
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from Core.permissions.OrganizerPermissions import IsOrganizerOwnerProfile

from ..models.tour_organizer import TourOrganizer

from django.core import exceptions

from collections import defaultdict

from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(
        summary="List of All Organizers who participate in Advertiser Offers", tags=["Organizer Data"]),
    retrieve=extend_schema(
        summary="Retrieve Organizer Profile", tags=["Organizer Data"]),
    update=extend_schema(summary="Update Organizer Data",
                         tags=["Organizer Data"]),
)
class TourOrganizerView(UserViewSet):
    serializer_class = UserSerializer
    organizer_serializer_class = TourOrganizerSerializer
    permission_classes = [IsOrganizerOwnerProfile]

    def list(self, request):
        # get organziers who subscripe in advertisers offers
        try:
            advertiser = request.user.advertiser
            offers = advertiser.offers.all()
            offer_requests = OfferRequest.objects.filter(
                offer_object__in=offers, status='A'
            ).select_related('offer_point', 'offer_point__tour_object', 'offer_point__tour_object__tour_organizer')

            organizers = set()
            for offer_request in offer_requests:
                organizers.add(
                    offer_request.offer_point.tour_object.tour_organizer)

            serializer = self.organizer_serializer_class(
                list(organizers), many=True)
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        except exceptions.ObjectDoesNotExist as e:
            return Response({
                'errors': str(e)
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError as e:
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

    def retrieve(self, request, id):
        """
        Retrieve the organizer data by id.

        This method returns the serialized data of the TourOrganizer instance associated with the authenticated user.
        It checks if all fields in the serialized data have a value (not None) and sets the data_status accordingly.

        Returns:
            Response: Serialized data of the organizer and status indicating the data_status.
        """
        try:
            organizer = TourOrganizer.objects.get(pk=id)
            serializer = self.organizer_serializer_class(organizer)

            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Orgnaizer does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, id):
        """
        Update the organizer data by id.

        This method allows updating the user and organizer data associated with the authenticated user.
        It performs partial updates on the user and organizer instances based on the provided request data.

        Args:
            id (int) : id of the organizer
            request (Request): The HTTP request containing the updated user and organizer data.
            request contain to dictionaries :
                user => contain user data [phone , email , username] for updating and send email when user change his email
                organizer => contain organizer data [address , evaluation , situation , logo]

        Returns:
            Response: Serialized data of the updated organizer or error response if validation or update fails.
        """
        try:
            user = request.user
            organizer = TourOrganizer.objects.get(pk=id)
            user_serializer = self.serializer_class(user)
            organizer_serializer = self.organizer_serializer_class(organizer)
            errors = []

            # don't forget to apply SRP
            if 'user' in request.data and request.data['user']:
                user_serializer = self.serializer_class(
                    user, data=request.data['user'], partial=True)
                if not user_serializer.is_valid(raise_exception=False):
                    errors.append(user_serializer.errors)
                else:
                    self.perform_update(user_serializer)

            if 'organizer' in request.data:
                organizer_serializer = self.organizer_serializer_class(
                    organizer, data=request.data['organizer'], partial=True)
                if not organizer_serializer.is_valid(raise_exception=False):
                    errors.append(organizer_serializer.errors)
                else:
                    organizer_serializer.save()

            if 'logo' in request.data:
                organizer_serializer = self.organizer_serializer_class(
                    organizer, data=request.data, partial=True)
                if not organizer_serializer.is_valid():
                    errors.append(organizer_serializer.errors)
                else:
                    organizer_serializer.save()

            if errors:
                raise ValidationError(errors)

            return Response(
                {
                    'data': organizer_serializer.data,
                    'message': 'Organizer Updated Successfully'
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Orgnaizer does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(

    list=extend_schema(summary="Get All Organizer Statstics",
                       tags=["Organizer Statistics"]),

)
class OrganizerStatistics(ModelViewSet):
    def list(self, request):
        # don't forget to apply SRP
        try:

            organizer = request.user.organizer
            tours = organizer.organizer_tours.filter(posted=1).all()

            months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
            tours_per_month = {
                month: 0 for month in months
            }
            profits_per_month = {
                month: 0 for month in months
            }

            result = []
            total_profit = sum(tour.seat_num*tour.seat_cost for tour in tours)
            for tour in tours:
                tours_per_month[tour.start_date.strftime("%B")] += 1
                profits_per_month[tour.start_date.strftime(
                    "%B")] += tour.seat_num * tour.seat_cost

            for month, count in tours_per_month.items():
                profits_per_month[month] = round(profits_per_month[month] /
                                                 total_profit * 100, 2)
                data = {"month": month, "count": count,
                        "profits_per_month": f"{profits_per_month[month]}%"}
                result.append(data)

            comments = []

            for tour in tours:
                for comment in tour.tour_comments.all():
                    comments.append(comment)

            organizer_tours_rating = get_sentiment_scores(comments)

            data = {
                "tour_per_months": result,
                "organizer_tours_rating": organizer_tours_rating
            }

            return Response({"data": data}, status=status.HTTP_200_OK)
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Tour does not exist!"
            },
                status=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError as e:
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

    def get_organizer_tour_profits_per_month(self, tour_organizer):
        """
        Calculates the profits for an organizer's tours per month.

        Args:
            tour_organizer (TourOrganizer): The tour organizer object.

        Returns:
            dict: A dictionary where the keys are the month-year strings and the values are the profits for that month.
        """
        profits_per_month = defaultdict(int)

        tours = tour_organizer.organizer_tours.filter(posted=1)
        tour_profits = 0

        for tour in tours:
            month_name = tour.start_date.strftime('%d')

            tour_profit += tour.seat_num * tour.seat_cost

            profits_per_month[month_name] += tour_profits

        return profits_per_month


def get_sentiment_scores(comments):
    """
    Calculates sentiment scores for a list of comments using the SentimentIntensityAnalyzer.

    Args:
        comments (list): A list of Comment objects or strings representing comments.

    Returns:
        list: A list of compound sentiment scores for each comment.
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = []
    result = 0
    if len(comments) > 0:
        for comment in comments:
            sentiment_scores = analyzer.polarity_scores(comment.comment)
            compound_score = sentiment_scores['compound']
            scores.append(compound_score)
        result = convert_to_percentage_value(scores)
    else:
        result = 0

    return f"{round(result, 2)}%"


def convert_to_percentage_value(values):
    """
    Converts a list of values from the range [-1, 1] to the range [0, 5].
    the range in we have in [-1,1] so we add 1 to make it in [0 ,2] then we multipal it with 2.5
    to make it [0,5] to apply 5 star system
    then we converte the last result to percentage value

    Args:
        values (list): A list of numeric values representing ratings within the range [-1, 1].

    Returns:
        float: The average rating in percentage.
    """
    total = 0
    for value in values:
        rating = round((value + 1) * 2.5, 1)
        total += rating
    average_rating = round(total / len(values), 1)
    average_rating = average_rating * 100 / 5
    return average_rating
