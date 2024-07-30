from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from django.core import exceptions

from ..serializer.ReportSerializer import ReportSerializer
from ..models.report import ReportType
from Tour_Organizer.models.tour_organizer import TourOrganizer


@extend_schema_view(
    create_report=extend_schema(
        summary="Allowed for Clients and Advertisers to report to Orgnaizer", tags=['Report'])
)
class ReportView(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    @action(detail=False)
    def create_report(self, request, organizer_id):
        try:
            complainant = request.user
            report_type = self.specify_report_type(complainant)
            organizer = TourOrganizer.objects.prefetch_related(
                'user').get(pk=organizer_id)
            respondent = organizer.user
            data = {
                "reason": request.data['reason'],
                "report_type": report_type,
            }
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(respondent=respondent, complainant=complainant)

            return Response(
                {
                    'message': "Report Created Successfully"
                },
                status=status.HTTP_201_CREATED
            )
        except exceptions.ObjectDoesNotExist:
            return Response({
                'errors': "Organizer dose not exist!!"
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

    def specify_report_type(self, user):
        report_type = ""
        match user.role:
            case "C":
                report_type = ReportType.CLIENT_REPORT
            case "AD":
                report_type = ReportType.ADVERTISER_REPORT
            case _:
                pass
        return report_type
