from django.db import models
from .user import UserAccount

class Reports_Types (models.Model):
    """
    Model representing the types of reports.
    """
    type = models.CharField(max_length=150)
    
class Report (models.Model):
    """
    Model representing a report.

    Attribute:
    - reason (CharField) : The reason for the report.
    - respondent_id : The user being reported.
    - complainant_id : The user making the report.
    - type_id : The type of the report.
    """
    reason = models.CharField(
            max_length = 150,
            null = True
            )
    type_id = models.ForeignKey( 
        Reports_Types ,
        on_delete = models.CASCADE 
    )
    respondent_id = models.ForeignKey( 
        UserAccount ,
        on_delete = models.CASCADE 
    )
    complainant_id = models.ForeignKey( 
        UserAccount ,
        on_delete = models.CASCADE 
    )


