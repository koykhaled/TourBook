from django.db import models
from .base import BaseModel
from django.contrib.auth import get_user_model
User = get_user_model()


class ReportType(models.TextChoices):
    CLIENT_REPORT = "CR", "Client Report"
    ADVERTISER_REPORT = "AR", "Advertiser Report"


class Report (BaseModel):
    """
    Model representing a report.

    Attribute:
    - reason (CharField) : The reason for the report.
    - respondent : The user being reported.
    - complainant : The user making the report.
    - type : The type of the report.
    """
    reason = models.CharField(
        max_length=150,
        null=True
    )
    report_type = models.CharField(max_length=20, choices=ReportType.choices)

    respondent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="respondent"
    )
    complainant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="complainant"
    )
