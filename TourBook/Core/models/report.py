from django.db import models
from .user import UserAccount
from .base import BaseModel


class ReportTypes (BaseModel):
    """
    Model representing the types of reports.
    """
    type = models.CharField(max_length=150)


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
    type = models.ForeignKey(
        ReportTypes,
        on_delete=models.CASCADE
    )
    respondent = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="respondent"
    )
    complainant = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="complainant"
    )
