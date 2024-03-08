from django.db import models


class Base(models.Model):
    """
    Base model providing common fields and functionality.

    Fields:
        created_at (DateTimeField): The datetime when the object was created.
        updated_at (DateTimeField): The datetime when the object was last updated.

    Methods:
        get_char_fields(): Get a list of all CharField objects in the model.

    Example Usage:
        class MyModel(Base):
            name = models.CharField(max_length=255)
            description = models.TextField()

        my_model = MyModel(name='Example', description='Description')
        my_model.save()
    """
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)

    def get_char_fields(self):
        """
        Get a list of all CharField objects in the model.

        Returns:
            List[CharField]: A list of CharField objects in the model.
        """
        char_fields=[]
        fields=self._meta.get_fields()
        for field in fields :
            if(isinstance(field,models.CharField)):
                char_fields.append(field)
        
        return char_fields

