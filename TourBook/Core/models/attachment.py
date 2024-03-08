from django.db import models
class Attachment (models.Model):
    """
    Model representing an attachment.

    Attributes:
        key (str) : The key of the attachment stored in AWS.
        type (FileField) : The file attachment  (allowed types: JPG, PDF, JPEG, and PNG).
    """
    key = models.CharField(max_length=100)
    type = models.FileField(upload_to='attachments/')

    def clean(self):
        """
        Custom validation for the Attachment model.
        """
        super().clean()
        if self.type:
            file_extension = self.type.name.split('.')[-1].lower()
            allowed_extensions = ['jpg', 'pdf','jpeg','png']
            if file_extension not in allowed_extensions:
                raise ValueError('Invalid file type. Only JPG , PDF , JPEG and PNG files are allowed.')