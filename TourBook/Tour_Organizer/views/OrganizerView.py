from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


from ..serializers.TourOrganizerSerializer import TourOrganizerSerializer
from accounts.serializers import UserSerializer
from djoser.views import UserViewSet

from Core.permissions import IsOrganizer

from ..models.tour_organizer import TourOrganizer

from django.core import exceptions

from collections import defaultdict


class TourOrganizerView(UserViewSet):
    serializer_class = UserSerializer
    organizer_serializer_class = TourOrganizerSerializer
    permission_classes = [IsOrganizer]

    def get_organizer(self, request):
        """
        Retrieve the organizer data for the authenticated user.

        This method returns the serialized data of the TourOrganizer instance associated with the authenticated user.
        It checks if all fields in the serialized data have a value (not None) and sets the data_status accordingly.

        Returns:
            Response: Serialized data of the organizer and status indicating the data_status.
        """
        user = request.user
        data_status = 0
        organizer = TourOrganizer.objects.get(user=user)
        serializer = self.organizer_serializer_class(organizer)
        if all(value is not None for value in serializer.data.values()):
            data_status = 1

        return Response({
            "data": serializer.data,
            "status": data_status
        }, status=status.HTTP_200_OK)

    def update_organizer(self, request):
        """
        Update the organizer data for the authenticated user.

        This method allows updating the user and organizer data associated with the authenticated user.
        It performs partial updates on the user and organizer instances based on the provided request data.

        Args:
            request (Request): The HTTP request containing the updated user and organizer data.
            request contain to dictionaries :
                user => contain user data [phone , email , username] for updating and send email when user change his email
                organizer => contain organizer data [address , evaluation , situation , logo]

        Returns:
            Response: Serialized data of the updated organizer or error response if validation or update fails.
        """
        try:
            user = request.user
            organizer = TourOrganizer.objects.get(user=user)
            user_serializer = self.serializer_class(user)
            organizer_serializer = self.organizer_serializer_class(organizer)
            errors = []

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
        except Exception as e:
            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_organizer_statistics(self, request):
        try:
            organizer = request.user.organizer

            tours_per_month = organizer.organizer_tours.annotate(
                month=ExtractMonth('created_at')).values('month').annotate(count=Count('id'))

            profits_per_month = self.get_organizer_tour_profits_per_month(
                organizer)

            organizer_tour = organizer.organizer_tours.filter(
                posted=1, pk=request.data['tour_id']).get()

            comments = organizer_tour.tour_comments.all()

            if len(comments) > 0:
                sentiment_scores = get_sentiment_scores(comments)
                organizer_tour_rating = convert_to_percentage_value(
                    sentiment_scores)
            else:
                organizer_tour_rating = 0

            data = {
                'tours_per_month': tours_per_month,
                "organizer_tour_rating": organizer_tour_rating,
                'profits_per_month': profits_per_month
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
            month_name = tour.start_date.strftime('%B')
            tour_profits = tour.seat_num * tour.seat_cost
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
    for comment in comments:
        sentiment_scores = analyzer.polarity_scores(comment.comment)
        compound_score = sentiment_scores['compound']
        scores.append(compound_score)
    return scores


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
