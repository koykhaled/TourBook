from django.db import models
from datetime import datetime

# Create your models here.


class BaseModel(models.Model):
    """A base model representing common fields for other models.

    Attributes:
        created_at (datetime): The date and time when the record was created.
        updated_at (datetime): The date and time when the record was last updated.
    """
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_char_fields(self):
        char_fields = []
        fields = self._meta.get_fields()
        for field in fields:
            if isinstance(field, models.CharField):
                char_fields.append(field)
        return char_fields

    def get_numeric_fields(self):
        numeric_fields = []
        fields = self._meta.get_fields()
        for field in fields:
            if field.name != 'id' and isinstance(field, models.IntegerField) or isinstance(field, models.DecimalField):
                numeric_fields.append(field)

        return numeric_fields

    def is_within(self, min_value, max_value, value):
        return min_value <= value <= max_value

    def save(self, *args, **kwargs):
        created_at = datetime.now().replace(microsecond=0)
        self.created_at = datetime.strptime(
            str(created_at), "%Y-%m-%d %H:%M:%S")

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
